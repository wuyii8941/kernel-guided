"""
Kernel-Guided Fuzzing Benchmark - Original Strategy with Advanced Analytics
============================================================================

策略设计:
- **Guided 策略**: 80% 数据库采样 + 20% 基础随机变异（最原始、最稳健）
- **Random 基线**: 原始 FreeFuzz (20% 数据库采样)

高级分析功能 (保留):
- KernelClassifier: 区分 Compute Kernels (实) vs Dirty Kernels (虚)
- BugDepthAnalyzer: 区分 Shallow Bugs vs Deep Logic Bugs
- EnhancedCoverageTracker: Compute/Dirty 统计
- 完整可视化: 6 子图对比

设计理由:
- 实验证明 SurgicalMutationPatcher 和 AdaptiveMutationController 反而限制了搜索空间
- 原始的 "High DB Probability" 策略效果最好

Author: Research Team
Date: 2025-12-15
"""

import copy
import random
import configparser
import os
import json
import pickle
import shutil
import time
from os.path import join
from pathlib import Path
from typing import Set, List, Dict, Tuple, Optional
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import numpy as np

# FreeFuzz imports
from classes.database import TorchDatabase
from classes.torch_api import TorchAPI, TorchArgument
from classes.torch_library import TorchLibrary
from classes.argument import Argument, ArgType
from constants.enum import OracleType


# =============================================================================
# Kernel Classifier - 区分虚/实 Kernel
# =============================================================================

class KernelClassifier:
    """
    Kernel 分类器 - 区分 Compute Kernels (实) 和 Dirty Kernels (虚)
    
    虚 Kernel (Dirty): 错误检查、参数验证、内存拷贝等
    实 Kernel (Compute): 实际计算、backward、elementwise 等
    """
    
    DIRTY_PATTERNS = [
        'check', 'error', 'invalid', 'assert', 'validate', 'verify',
        'memcpy', 'memset', 'malloc', 'free', 'alloc',
        'copy', 'clone', 'empty', 'zeros', 'ones', 'full',
        'contiguous', 'reshape', 'view', 'expand', 'squeeze',
        'to_', 'type_', 'cast', 'convert',
    ]
    
    COMPUTE_PATTERNS = [
        'backward', 'forward', 'grad',
        'elementwise', 'kernel', 'launch',
        'matmul', 'gemm', 'conv', 'pool',
        'lstm', 'gru', 'rnn', 'attention',
        'softmax', 'sigmoid', 'relu', 'tanh', 'gelu',
        'dropout', 'norm', 'batch', 'layer',
        'reduce', 'sum', 'mean', 'max', 'min',
        'fused', 'optimized', 'cudnn', 'cublas',
    ]
    
    @staticmethod
    def is_dirty_kernel(kernel_name: str) -> bool:
        name_lower = kernel_name.lower()
        for pattern in KernelClassifier.DIRTY_PATTERNS:
            if pattern in name_lower:
                return True
        return False
    
    @staticmethod
    def get_compute_kernels(kernels: Set[str]) -> Set[str]:
        return {k for k in kernels if not KernelClassifier.is_dirty_kernel(k)}
    
    @staticmethod
    def get_dirty_kernels(kernels: Set[str]) -> Set[str]:
        return {k for k in kernels if KernelClassifier.is_dirty_kernel(k)}


# =============================================================================
# Bug Depth Analyzer - Bug 深度分析
# =============================================================================

class BugDepthAnalyzer:
    """Bug 深度分析器 - 区分 Shallow Bugs 和 Deep Logic Bugs"""
    
    SHALLOW_PATTERNS = [
        'type', 'argument', 'expected', 'got', 'invalid',
        'dimension', 'shape', 'size', 'mismatch',
        'not supported', 'not implement', 'cannot',
        'must be', 'should be', 'requires',
    ]
    
    DEEP_PATTERNS = [
        'cuda', 'kernel', 'launch', 'device',
        'backward', 'gradient', 'autograd',
        'nan', 'inf', 'overflow', 'underflow',
        'precision', 'numerical', 'accuracy',
        'internal assert', 'cublas', 'cudnn',
        'segfault', 'memory', 'corruption',
    ]
    
    @staticmethod
    def analyze_bug_depth(error_msg: str) -> str:
        if not error_msg:
            return "unknown"
        msg_lower = error_msg.lower()
        for pattern in BugDepthAnalyzer.DEEP_PATTERNS:
            if pattern in msg_lower:
                return "deep"
        for pattern in BugDepthAnalyzer.SHALLOW_PATTERNS:
            if pattern in msg_lower:
                return "shallow"
        return "unknown"
    
    @staticmethod
    def analyze_bug_file(bug_file: str) -> Dict:
        result = {"depth": "unknown", "has_backward": False, "has_kernel": False}
        try:
            with open(bug_file, 'r', errors='ignore') as f:
                content = f.read()
                content_lower = content.lower()
                result["has_backward"] = 'backward' in content_lower or 'grad' in content_lower
                result["has_kernel"] = 'kernel' in content_lower or 'cuda' in content_lower
                
                lines = content.strip().split('\n')
                for line in reversed(lines[-10:]):
                    if 'error' in line.lower() or 'exception' in line.lower():
                        result["depth"] = BugDepthAnalyzer.analyze_bug_depth(line)
                        break
                
                if result["depth"] == "unknown":
                    result["depth"] = "deep" if (result["has_backward"] or result["has_kernel"]) else "shallow"
        except:
            pass
        return result


# =============================================================================
# Safety Guards
# =============================================================================

class Speedometer:
    """速度监控"""
    def __init__(self, window_size: int = 100):
        self.timestamps = deque(maxlen=window_size)
        self.start_time = None
        self.total_iterations = 0
    
    def start(self):
        self.start_time = time.time()
    
    def tick(self):
        self.total_iterations += 1
        self.timestamps.append(time.time())
    
    def get_speed(self) -> float:
        if len(self.timestamps) < 2:
            return 0.0
        return (len(self.timestamps) - 1) / (self.timestamps[-1] - self.timestamps[0])
    
    def get_average_speed(self) -> float:
        if not self.start_time or self.total_iterations == 0:
            return 0.0
        return self.total_iterations / (time.time() - self.start_time)
    
    def format_time(self, seconds: float) -> str:
        if seconds == float('inf') or seconds < 0:
            return "Unknown"
        hours, rem = divmod(int(seconds), 3600)
        minutes, secs = divmod(rem, 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        return f"{secs}s"
    
    def get_status(self, current: int, total: int) -> str:
        speed = self.get_speed()
        avg = self.get_average_speed()
        eta = (total - current) / avg if avg > 0 else float('inf')
        elapsed = time.time() - self.start_time if self.start_time else 0
        return f"{speed:.1f} it/s | Elapsed: {self.format_time(elapsed)} | ETA: {self.format_time(eta)}"


class DiskGuard:
    """磁盘空间监控"""
    def __init__(self, output_dir: str, min_free_gb: float = 1.0):
        self.output_dir = Path(output_dir)
        self.min_free_gb = min_free_gb
    
    def check_and_cleanup(self) -> Tuple[bool, str]:
        stat = shutil.disk_usage(self.output_dir)
        free_gb = stat.free / (1024**3)
        if free_gb >= self.min_free_gb:
            return False, ""
        # 尝试清理
        for temp in self.output_dir.rglob("temp.py"):
            try:
                temp.unlink()
            except:
                pass
        stat = shutil.disk_usage(self.output_dir)
        free_gb = stat.free / (1024**3)
        if free_gb < self.min_free_gb:
            return True, f"CRITICAL: Only {free_gb:.2f} GB free"
        return False, ""
    
    def get_status(self) -> str:
        stat = shutil.disk_usage(self.output_dir)
        return f"{stat.free / (1024**3):.2f} GB free"


class OutlierFilter:
    """异常参数过滤"""
    def __init__(self, max_elements: int = int(1e8)):
        self.max_elements = max_elements
        self.filtered = 0
        self.total = 0
    
    def check_api(self, api) -> bool:
        self.total += 1
        for _, arg in api.args.items():
            if arg is None:
                continue
            if hasattr(arg, 'type') and arg.type == ArgType.TORCH_TENSOR:
                if hasattr(arg, 'shape') and arg.shape:
                    elements = 1
                    for d in arg.shape:
                        elements *= d
                    if elements > self.max_elements:
                        self.filtered += 1
                        return True
        return False


# =============================================================================
# Checkpoint Manager
# =============================================================================

class CheckpointManager:
    def __init__(self, checkpoint_dir: str, strategy: str, api_name: str):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file = self.checkpoint_dir / f"{api_name.replace('.', '_')}_{strategy}_ckpt.pkl"
    
    def save(self, data: dict) -> bool:
        try:
            with open(self.checkpoint_file, 'wb') as f:
                pickle.dump(data, f)
            return True
        except:
            return False
    
    def load(self) -> Optional[dict]:
        if not self.checkpoint_file.exists():
            return None
        try:
            with open(self.checkpoint_file, 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def exists(self) -> bool:
        return self.checkpoint_file.exists()
    
    def clear(self):
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()


# =============================================================================
# Bug Tracker - 支持深度分析
# =============================================================================

class BugTracker:
    def __init__(self, name: str, output_dir: str):
        self.name = name
        self.output_dir = output_dir
        self.bugs = {"crash": [], "cuda": [], "precision": []}
        self.bug_files = {"crash": set(), "cuda": set(), "precision": set()}
        self.depth_stats = {"deep": 0, "shallow": 0, "unknown": 0}
    
    def scan_bugs(self):
        oracle_map = {"crash": "crash-oracle", "cuda": "cuda-oracle", "precision": "precision-oracle"}
        for bug_type, oracle_name in oracle_map.items():
            bug_dir = join(self.output_dir, oracle_name, "potential-bug")
            if os.path.exists(bug_dir):
                for root, _, files in os.walk(bug_dir):
                    for f in files:
                        if f.endswith('.py'):
                            path = join(root, f)
                            if path not in self.bug_files[bug_type]:
                                self.bug_files[bug_type].add(path)
                                depth = BugDepthAnalyzer.analyze_bug_file(path)["depth"]
                                self.depth_stats[depth] += 1
                                self.bugs[bug_type].append((len(self.bugs[bug_type]), path, depth))
    
    def get_total_bugs(self) -> int:
        return sum(len(b) for b in self.bugs.values())
    
    def get_bugs_by_type(self, t: str) -> int:
        return len(self.bugs.get(t, []))
    
    def get_deep_bugs(self) -> int:
        return self.depth_stats["deep"]
    
    def get_shallow_bugs(self) -> int:
        return self.depth_stats["shallow"]
    
    def print_summary(self):
        print(f"\n[{self.name}] Bugs: Total={self.get_total_bugs()} | "
              f"CRASH={self.get_bugs_by_type('crash')} | CUDA={self.get_bugs_by_type('cuda')} | "
              f"PRECISION={self.get_bugs_by_type('precision')}")
        print(f"         Deep={self.get_deep_bugs()} | Shallow={self.get_shallow_bugs()}")


# =============================================================================
# Enhanced Coverage Tracker - 支持 Kernel 分类
# =============================================================================

class EnhancedCoverageTracker:
    def __init__(self, name: str):
        self.name = name
        self.all_kernels: Set[str] = set()
        self.kernel_provenance: Dict[str, int] = {}
        self.history: List[Tuple[int, int]] = []
        self.compute_history: List[Tuple[int, int]] = []
    
    def update(self, new_kernels: Set[str], iteration: int) -> int:
        if not isinstance(new_kernels, set):
            new_kernels = set(new_kernels) if new_kernels else set()
        
        fresh = new_kernels - self.all_kernels
        if fresh:
            for k in fresh:
                self.kernel_provenance[k] = iteration
            self.all_kernels.update(fresh)
            print(f"  [{self.name}] Iter {iteration}: +{len(fresh)} kernels! Total: {len(self.all_kernels)}")
        
        self.history.append((iteration, len(self.all_kernels)))
        self.compute_history.append((iteration, len(KernelClassifier.get_compute_kernels(self.all_kernels))))
        return len(fresh)
    
    def get_total(self) -> int:
        return len(self.all_kernels)
    
    def get_compute_total(self) -> int:
        return len(KernelClassifier.get_compute_kernels(self.all_kernels))
    
    def get_dirty_total(self) -> int:
        return len(KernelClassifier.get_dirty_kernels(self.all_kernels))
    
    def get_exclusive(self, other: 'EnhancedCoverageTracker') -> Set[str]:
        return self.all_kernels - other.all_kernels


# =============================================================================
# Evolutionary Corpus
# =============================================================================

class EvolutionaryCorpus:
    def __init__(self, max_size: int = 100):
        self.corpus: List[TorchAPI] = []
        self.max_size = max_size
    
    def add_seed(self, api: TorchAPI):
        self.corpus.append(copy.deepcopy(api))
        if len(self.corpus) > self.max_size:
            self.corpus.pop(0)
    
    def select_parent(self) -> Optional[TorchAPI]:
        return random.choice(self.corpus) if self.corpus else None
    
    def size(self) -> int:
        return len(self.corpus)
    
    def clear(self):
        self.corpus.clear()


# =============================================================================
# Probability Patcher (唯一的 Guided 增强)
# =============================================================================

_ORIGINAL_DO_SELECT_FROM_DB = None

class ProbabilityPatcher:
    """
    将数据库采样概率从 20% 提升到 80%
    
    这是 Guided 策略的**唯一**增强，保持最原始的变异逻辑
    """
    
    @staticmethod
    def patch_high_db_probability():
        import utils.probability as prob_module
        global _ORIGINAL_DO_SELECT_FROM_DB
        _ORIGINAL_DO_SELECT_FROM_DB = prob_module.do_select_from_db
        
        def high_db_select() -> bool:
            from numpy.random import rand
            return rand() < 0.8
        
        prob_module.do_select_from_db = high_db_select
        print("[Patch] ✅ Database sampling: 20% → 80%")
    
    @staticmethod
    def restore():
        global _ORIGINAL_DO_SELECT_FROM_DB
        if _ORIGINAL_DO_SELECT_FROM_DB:
            import utils.probability as prob_module
            prob_module.do_select_from_db = _ORIGINAL_DO_SELECT_FROM_DB
            _ORIGINAL_DO_SELECT_FROM_DB = None
            print("[Patch] 🔄 Database sampling restored")


# =============================================================================
# Enhanced Fuzzer (原始策略版本)
# =============================================================================

class EnhancedFuzzer:
    """
    增强型 Fuzzer - 使用最原始的变异策略
    
    Guided 增强:
    - 80% 数据库采样（通过 ProbabilityPatcher）
    - 进化 Corpus（保留发现新 Kernel 的种子）
    - 停滞重置（防止死循环）
    
    不使用:
    - SurgicalMutationPatcher（参数约束）
    - AdaptiveMutationController（动态调整）
    """
    
    def __init__(self, api_name: str, output_dir: str, strategy_name: str,
                 enable_corpus: bool = False, use_all_oracles: bool = True):
        self.api_name = api_name
        self.output_dir = output_dir
        self.strategy_name = strategy_name
        self.enable_corpus = enable_corpus
        
        os.makedirs(output_dir, exist_ok=True)
        
        self.coverage = EnhancedCoverageTracker(strategy_name)
        self.bug_tracker = BugTracker(strategy_name, output_dir)
        self.corpus = EvolutionaryCorpus() if enable_corpus else None
        self.library = TorchLibrary(output_dir)
        
        self.oracles = [OracleType.CRASH, OracleType.CUDA, OracleType.PRECISION] if use_all_oracles else [OracleType.CRASH]
        
        self.speedometer = Speedometer()
        self.disk_guard = DiskGuard(output_dir)
        self.outlier_filter = OutlierFilter()
        self.checkpoint_mgr = CheckpointManager(output_dir, strategy_name.lower(), api_name)
        
        # 停滞重置
        self.stagnation_counter = 0
        self.stagnation_threshold = 50
        self.stagnation_resets = 0
        
        print(f"[Fuzzer] {strategy_name} | Corpus: {enable_corpus} | Oracles: {len(self.oracles)}")
    
    def run_fuzzing_loop(self, max_iterations: int = 10000, checkpoint_interval: int = 100):
        self.speedometer.start()
        start_iteration = 0
        
        # 恢复检查点
        if self.checkpoint_mgr.exists():
            data = self.checkpoint_mgr.load()
            if data:
                self.coverage.all_kernels = data.get('kernels', set())
                start_iteration = data.get('iteration', 0) + 1
                if self.corpus and data.get('corpus'):
                    self.corpus.corpus = data['corpus']
                print(f"✅ Resuming from iteration {start_iteration}")
        
        print(f"\n{'='*70}")
        print(f"Starting {self.strategy_name}: {start_iteration} → {max_iterations}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        for i in range(start_iteration, max_iterations):
            self.speedometer.tick()
            
            # 生成测试用例
            if self.corpus and self.corpus.size() > 0 and random.random() < 0.7:
                api = copy.deepcopy(self.corpus.select_parent())
                api.mutate()  # 使用原始变异
            else:
                api = TorchAPI(self.api_name)
                api.mutate()  # 使用原始变异
            
            # 过滤异常
            if self.outlier_filter.check_api(api):
                continue
            
            # 执行测试
            all_kernels = set()
            for oracle in self.oracles:
                try:
                    kernels = self.library.test_with_oracle(api, oracle)
                    if kernels:
                        all_kernels.update(kernels)
                except:
                    pass
            
            # 更新覆盖率
            new_count = self.coverage.update(all_kernels, i)
            
            # 停滞重置机制
            if new_count > 0:
                self.stagnation_counter = 0
                if self.corpus:
                    self.corpus.add_seed(api)
            else:
                self.stagnation_counter += 1
                if self.stagnation_counter >= self.stagnation_threshold:
                    self.stagnation_resets += 1
                    self.stagnation_counter = 0
                    if self.corpus:
                        self.corpus.clear()
                    print(f"  🔄 [{self.strategy_name}] STAGNATION RESET #{self.stagnation_resets}")
            
            # Bug 扫描
            if (i + 1) % 50 == 0:
                prev = self.bug_tracker.get_total_bugs()
                self.bug_tracker.scan_bugs()
                if self.bug_tracker.get_total_bugs() > prev:
                    print(f"  🐛 [{self.strategy_name}] New bugs found!")
            
            # 检查点
            if (i + 1) % checkpoint_interval == 0:
                self.checkpoint_mgr.save({
                    'iteration': i,
                    'kernels': self.coverage.all_kernels,
                    'corpus': self.corpus.corpus if self.corpus else None
                })
                
                critical, msg = self.disk_guard.check_and_cleanup()
                if critical:
                    print(f"❌ {msg}")
                    break
                
                elapsed = time.time() - start_time
                print(f"\n--- Checkpoint {i+1}/{max_iterations} ({elapsed/60:.1f}m) ---")
                print(f"Kernels: {self.coverage.get_total()} (Compute: {self.coverage.get_compute_total()})")
                print(f"Speed: {self.speedometer.get_status(i, max_iterations)}")
                if self.corpus:
                    print(f"Corpus: {self.corpus.size()}")
        
        self.checkpoint_mgr.clear()
        
        print(f"\n{'='*70}")
        print(f"{self.strategy_name} completed in {(time.time() - start_time)/60:.1f} min")
        print(f"{'='*70}")
        
        return self.coverage
    
    def print_stats(self):
        print(f"\n{'='*70}")
        print(f"STATS: {self.strategy_name}")
        print(f"{'='*70}")
        print(f"Kernels: {self.coverage.get_total()} | Compute: {self.coverage.get_compute_total()} | Dirty: {self.coverage.get_dirty_total()}")
        if self.stagnation_resets > 0:
            print(f"Stagnation Resets: {self.stagnation_resets}")
        self.bug_tracker.scan_bugs()
        self.bug_tracker.print_summary()


# =============================================================================
# Visualization - 完整 6 子图
# =============================================================================

def plot_full_oracle_results(
    random_coverage: EnhancedCoverageTracker,
    guided_coverage: EnhancedCoverageTracker,
    random_bugs: BugTracker,
    guided_bugs: BugTracker,
    api_name: str,
    output_dir: str
):
    """绘制完整的结果对比图（6 子图）"""
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    # A) Kernel 覆盖率曲线
    ax1 = fig.add_subplot(gs[0, :2])
    
    if random_coverage.history:
        iters, kernels = zip(*random_coverage.history)
        ax1.plot(iters, kernels, label=f"Random All: {random_coverage.get_total()}",
                color="#3498db", linewidth=2, alpha=0.6, linestyle='--')
    if guided_coverage.history:
        iters, kernels = zip(*guided_coverage.history)
        ax1.plot(iters, kernels, label=f"Guided All: {guided_coverage.get_total()}",
                color="#e74c3c", linewidth=2, alpha=0.6, linestyle='--')
    if random_coverage.compute_history:
        iters, kernels = zip(*random_coverage.compute_history)
        ax1.plot(iters, kernels, label=f"Random Compute: {random_coverage.get_compute_total()}",
                color="#3498db", linewidth=3)
    if guided_coverage.compute_history:
        iters, kernels = zip(*guided_coverage.compute_history)
        ax1.plot(iters, kernels, label=f"Guided Compute: {guided_coverage.get_compute_total()}",
                color="#e74c3c", linewidth=3)
    
    ax1.set_xlabel("Iteration", fontsize=11)
    ax1.set_ylabel("Cumulative Kernels", fontsize=11)
    ax1.set_title("A) Kernel Coverage (Solid=Compute, Dashed=All)", fontsize=12, fontweight='bold')
    ax1.legend(loc="lower right", fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # B) Kernel 分类
    ax2 = fig.add_subplot(gs[0, 2])
    categories = ['Compute', 'Dirty', 'Total']
    random_counts = [random_coverage.get_compute_total(), random_coverage.get_dirty_total(), random_coverage.get_total()]
    guided_counts = [guided_coverage.get_compute_total(), guided_coverage.get_dirty_total(), guided_coverage.get_total()]
    
    x = np.arange(len(categories))
    width = 0.35
    ax2.bar(x - width/2, random_counts, width, label='Random', color='#3498db', alpha=0.8)
    ax2.bar(x + width/2, guided_counts, width, label='Guided', color='#e74c3c', alpha=0.8)
    ax2.set_title("B) Kernel Classification", fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for i, (rc, gc) in enumerate(zip(random_counts, guided_counts)):
        ax2.text(i - width/2, rc + 0.5, str(rc), ha='center', fontsize=9)
        ax2.text(i + width/2, gc + 0.5, str(gc), ha='center', fontsize=9)
    
    # C) Bug 类型
    ax3 = fig.add_subplot(gs[1, 0])
    bug_types = ['CRASH', 'CUDA', 'PRECISION']
    random_bug_counts = [random_bugs.get_bugs_by_type(t.lower()) for t in bug_types]
    guided_bug_counts = [guided_bugs.get_bugs_by_type(t.lower()) for t in bug_types]
    
    x = np.arange(len(bug_types))
    ax3.bar(x - width/2, random_bug_counts, width, label='Random', color='#3498db', alpha=0.8)
    ax3.bar(x + width/2, guided_bug_counts, width, label='Guided', color='#e74c3c', alpha=0.8)
    ax3.set_title("C) Bugs by Type", fontsize=12, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(bug_types)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # D) Bug 深度
    ax4 = fig.add_subplot(gs[1, 1])
    depth_categories = ['Deep', 'Shallow', 'Total']
    random_depth = [random_bugs.get_deep_bugs(), random_bugs.get_shallow_bugs(), random_bugs.get_total_bugs()]
    guided_depth = [guided_bugs.get_deep_bugs(), guided_bugs.get_shallow_bugs(), guided_bugs.get_total_bugs()]
    
    x = np.arange(len(depth_categories))
    ax4.bar(x - width/2, random_depth, width, label='Random', color='#3498db', alpha=0.8)
    ax4.bar(x + width/2, guided_depth, width, label='Guided', color='#e74c3c', alpha=0.8)
    ax4.set_title("D) Bug Depth Analysis", fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(depth_categories)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # E) 发现速率
    ax5 = fig.add_subplot(gs[1, 2])
    window = max(50, len(random_coverage.history) // 20) if random_coverage.history else 50
    
    def calc_rates(history, window):
        rates = []
        for i in range(window, len(history), window):
            prev, curr = history[i-window][1], history[i][1]
            rates.append((history[i][0], (curr - prev) / window))
        return rates
    
    random_rates = calc_rates(random_coverage.compute_history, window)
    guided_rates = calc_rates(guided_coverage.compute_history, window)
    
    if random_rates:
        iters, rates = zip(*random_rates)
        ax5.plot(iters, rates, label="Random", color="#3498db", linewidth=2, marker='o', markersize=3)
    if guided_rates:
        iters, rates = zip(*guided_rates)
        ax5.plot(iters, rates, label="Guided", color="#e74c3c", linewidth=2, marker='s', markersize=3)
    
    ax5.set_title("E) Compute Kernel Discovery Rate", fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # F) 综合统计表
    ax6 = fig.add_subplot(gs[2, :])
    ax6.axis('off')
    
    compute_ratio = guided_coverage.get_compute_total() / max(random_coverage.get_compute_total(), 1)
    deep_ratio = guided_bugs.get_deep_bugs() / max(random_bugs.get_deep_bugs(), 1)
    
    table_data = [
        ["Metric", "Random", "Guided", "Ratio", "Insight"],
        ["All Kernels", f"{random_coverage.get_total()}", f"{guided_coverage.get_total()}",
         f"{guided_coverage.get_total()/max(random_coverage.get_total(),1):.2f}x", "Raw count"],
        ["🎯 Compute Kernels", f"{random_coverage.get_compute_total()}", f"{guided_coverage.get_compute_total()}",
         f"{compute_ratio:.2f}x", "TRUE coverage"],
        ["🗑️ Dirty Kernels", f"{random_coverage.get_dirty_total()}", f"{guided_coverage.get_dirty_total()}",
         f"{guided_coverage.get_dirty_total()/max(random_coverage.get_dirty_total(),1):.2f}x", "Noise"],
        ["Total Bugs", f"{random_bugs.get_total_bugs()}", f"{guided_bugs.get_total_bugs()}",
         f"{guided_bugs.get_total_bugs()/max(random_bugs.get_total_bugs(),1):.2f}x", "Raw count"],
        ["🎯 Deep Bugs", f"{random_bugs.get_deep_bugs()}", f"{guided_bugs.get_deep_bugs()}",
         f"{deep_ratio:.2f}x", "TRUE quality"],
        ["📋 Shallow Bugs", f"{random_bugs.get_shallow_bugs()}", f"{guided_bugs.get_shallow_bugs()}",
         f"{guided_bugs.get_shallow_bugs()/max(random_bugs.get_shallow_bugs(),1):.2f}x", "Entry errors"],
    ]
    
    table = ax6.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.22, 0.13, 0.13, 0.12, 0.40])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.2)
    
    for i in range(5):
        table[(0, i)].set_facecolor('#34495e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    for row in [2, 5]:
        for col in range(5):
            table[(row, col)].set_facecolor('#e8f6e8')
    
    ax6.set_title("F) Comprehensive Analysis", fontsize=13, fontweight='bold', pad=20)
    
    fig.suptitle(f"Kernel-Guided Fuzzing: {api_name}\nOriginal Strategy: 80% DB Sampling + Standard Mutation",
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    plot_file = join(output_dir, f"{api_name.replace('.', '_')}_analysis.png")
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n📊 Plot saved: {plot_file}")
    
    # Key Insights
    print(f"\n{'='*70}")
    print("📈 KEY INSIGHTS")
    print(f"{'='*70}")
    print(f"Compute Kernel Ratio (Guided/Random): {compute_ratio:.2f}x")
    print(f"Deep Bug Ratio (Guided/Random):       {deep_ratio:.2f}x")
    if compute_ratio > 1.0:
        print("✅ Guided discovers MORE real compute paths")
    if deep_ratio > 1.0:
        print("✅ Guided finds MORE deep logic bugs")


# =============================================================================
# Main Experiment Runner
# =============================================================================

def run_full_oracle_experiment(
    api_name: str,
    max_iterations: int,
    output_dir: str,
    config_file: str = "demo_torch.conf"
):
    """运行完整实验 - 原始策略版本"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 配置数据库
    config = configparser.ConfigParser()
    for path in [join("config", config_file), join("..", "config", config_file), config_file]:
        if os.path.exists(path):
            config.read(path)
            print(f"📝 Config: {os.path.abspath(path)}")
            break
    else:
        print("❌ Config file not found")
        return None
    
    TorchDatabase.database_config(
        config["mongodb"]["host"],
        int(config["mongodb"]["port"]),
        config["mongodb"]["torch_database"]
    )
    
    # =========================================================================
    # Phase 1: Random Baseline
    # =========================================================================
    print("\n" + "="*70)
    print("PHASE 1: RANDOM BASELINE (Original FreeFuzz)")
    print("="*70)
    
    random_fuzzer = EnhancedFuzzer(
        api_name=api_name,
        output_dir=join(output_dir, "random"),
        strategy_name="Random",
        enable_corpus=False,  # Random 不使用 Corpus
        use_all_oracles=True
    )
    
    random_coverage = random_fuzzer.run_fuzzing_loop(
        max_iterations=max_iterations,
        checkpoint_interval=max(100, max_iterations // 20)
    )
    random_fuzzer.print_stats()
    
    # =========================================================================
    # Phase 2: Guided Strategy (仅 80% DB 采样)
    # =========================================================================
    print("\n" + "="*70)
    print("PHASE 2: KERNEL-GUIDED (80% DB Sampling Only)")
    print("="*70)
    
    # 只应用数据库采样概率补丁
    ProbabilityPatcher.patch_high_db_probability()
    
    guided_fuzzer = EnhancedFuzzer(
        api_name=api_name,
        output_dir=join(output_dir, "guided"),
        strategy_name="Guided",
        enable_corpus=True,  # Guided 使用 Corpus
        use_all_oracles=True
    )
    
    try:
        guided_coverage = guided_fuzzer.run_fuzzing_loop(
            max_iterations=max_iterations,
            checkpoint_interval=max(100, max_iterations // 20)
        )
        guided_fuzzer.print_stats()
    finally:
        ProbabilityPatcher.restore()
    
    # =========================================================================
    # Visualization
    # =========================================================================
    plot_full_oracle_results(
        random_coverage, guided_coverage,
        random_fuzzer.bug_tracker, guided_fuzzer.bug_tracker,
        api_name, output_dir
    )
    
    # =========================================================================
    # Save Results
    # =========================================================================
    results = {
        "api": api_name,
        "max_iterations": max_iterations,
        "strategy": "Original: 80% DB Sampling + Standard Mutation",
        "random": {
            "total_kernels": random_coverage.get_total(),
            "compute_kernels": random_coverage.get_compute_total(),
            "dirty_kernels": random_coverage.get_dirty_total(),
            "bugs": {
                "total": random_fuzzer.bug_tracker.get_total_bugs(),
                "deep": random_fuzzer.bug_tracker.get_deep_bugs(),
                "shallow": random_fuzzer.bug_tracker.get_shallow_bugs(),
            }
        },
        "guided": {
            "total_kernels": guided_coverage.get_total(),
            "compute_kernels": guided_coverage.get_compute_total(),
            "dirty_kernels": guided_coverage.get_dirty_total(),
            "bugs": {
                "total": guided_fuzzer.bug_tracker.get_total_bugs(),
                "deep": guided_fuzzer.bug_tracker.get_deep_bugs(),
                "shallow": guided_fuzzer.bug_tracker.get_shallow_bugs(),
            },
            "stagnation_resets": guided_fuzzer.stagnation_resets
        },
        "ratios": {
            "compute_kernel": guided_coverage.get_compute_total() / max(random_coverage.get_compute_total(), 1),
            "deep_bug": guided_fuzzer.bug_tracker.get_deep_bugs() / max(random_fuzzer.bug_tracker.get_deep_bugs(), 1),
        }
    }
    
    result_file = join(output_dir, f"{api_name.replace('.', '_')}_results.json")
    with open(result_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved: {result_file}")
    return results


# =============================================================================
# Main
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Kernel-Guided Fuzzing - Original Strategy")
    parser.add_argument("--api", type=str, default="torch.nn.LSTM", help="API to test")
    parser.add_argument("--max-iterations", type=int, default=10000, help="Max iterations")
    parser.add_argument("--output", type=str, default="original_output", help="Output directory")
    parser.add_argument("--conf", type=str, default="demo_torch.conf", help="Config file")
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔬 KERNEL-GUIDED FUZZING (Original Strategy)")
    print("="*70)
    print(f"API: {args.api}")
    print(f"Max Iterations: {args.max_iterations:,}")
    print(f"Strategy: 80% DB Sampling + Standard Mutation (No Constraints)")
    print("="*70)
    
    run_full_oracle_experiment(
        api_name=args.api,
        max_iterations=args.max_iterations,
        output_dir=args.output,
        config_file=args.conf
    )


if __name__ == "__main__":
    main()