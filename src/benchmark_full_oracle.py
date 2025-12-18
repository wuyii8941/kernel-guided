"""
Kernel-Guided Fuzzing Benchmark - Full Oracle Edition with Hybrid Strategy
==========================================================================

核心增强:
1. **混合策略**: ε-greedy (90% 微创 + 10% 探索)
2. **动态变异**: 停滞时自动扩大变异范围
3. **取消饱和停止**: 改为"扩大搜索"而非"终止"
4. **全 Oracle 支持**: CRASH + CUDA + PRECISION

Author: Research Team
Date: 2025-12-13
"""

import copy
import random
import configparser
import os
import json
import hashlib
import re
import pickle
import shutil
from os.path import join
from pathlib import Path
from typing import Set, List, Dict, Tuple, Optional
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import numpy as np
import time

# FreeFuzz imports
from classes.database import TorchDatabase
from classes.torch_api import TorchAPI, TorchArgument
from classes.torch_library import TorchLibrary
from classes.argument import Argument, ArgType
from constants.enum import OracleType


# =============================================================================
# Safety Guards (保护机制)
# =============================================================================

class Speedometer:
    """速度监控 - 及时发现性能问题"""
    def __init__(self, window_size: int = 100, slow_threshold: float = 0.5):
        self.window_size = window_size
        self.slow_threshold = slow_threshold
        self.timestamps = deque(maxlen=window_size)
        self.start_time = None
        self.total_iterations = 0
        self.slow_warnings = 0
    
    def start(self):
        self.start_time = time.time()
        self.timestamps.append(self.start_time)
    
    def tick(self):
        self.total_iterations += 1
        self.timestamps.append(time.time())
    
    def get_speed(self) -> float:
        if len(self.timestamps) < 2:
            return 0.0
        elapsed = self.timestamps[-1] - self.timestamps[0]
        return (len(self.timestamps) - 1) / elapsed if elapsed > 0 else 0.0
    
    def get_average_speed(self) -> float:
        if not self.start_time or self.total_iterations == 0:
            return 0.0
        elapsed = time.time() - self.start_time
        return self.total_iterations / elapsed if elapsed > 0 else 0.0
    
    def estimate_remaining_time(self, current_iter: int, max_iter: int) -> float:
        avg_speed = self.get_average_speed()
        if avg_speed == 0:
            return float('inf')
        return (max_iter - current_iter) / avg_speed
    
    def check_speed(self) -> Tuple[bool, str]:
        current_speed = self.get_speed()
        if current_speed < self.slow_threshold:
            self.slow_warnings += 1
            warning = (f"⚠️  SLOW SPEED: {current_speed:.2f} it/s (threshold: {self.slow_threshold})")
            if current_speed < 0.1:
                warning += "\n   → Check if Precision Oracle is too slow"
            elif current_speed < 0.5:
                warning += "\n   → Consider reducing complexity or disabling oracles"
            return True, warning
        return False, ""
    
    def format_time(self, seconds: float) -> str:
        if seconds == float('inf'):
            return "Unknown"
        hours, minutes, secs = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        return f"{secs}s"
    
    def get_status(self, current_iter: int, max_iter: int) -> str:
        current_speed = self.get_speed()
        avg_speed = self.get_average_speed()
        remaining = self.estimate_remaining_time(current_iter, max_iter)
        elapsed = time.time() - self.start_time if self.start_time else 0
        return (f"{current_speed:.2f} it/s (avg: {avg_speed:.2f}) | "
                f"Elapsed: {self.format_time(elapsed)} | ETA: {self.format_time(remaining)}")


class DiskGuard:
    """磁盘空间监控 - 防止爆满崩溃"""
    def __init__(self, output_dir: str, min_free_gb: float = 1.0, auto_cleanup: bool = True):
        self.output_dir = Path(output_dir)
        self.min_free_gb = min_free_gb
        self.auto_cleanup = auto_cleanup
        self.warnings = 0
        self.cleanups = 0
    
    def get_disk_usage(self) -> Tuple[float, float, float]:
        stat = shutil.disk_usage(self.output_dir)
        return (stat.total / (1024**3), stat.used / (1024**3), stat.free / (1024**3))
    
    def check_space(self) -> Tuple[bool, str]:
        total, used, free = self.get_disk_usage()
        if free < self.min_free_gb:
            self.warnings += 1
            warning = f"⚠️  DISK SPACE: Only {free:.2f} GB free (threshold: {self.min_free_gb} GB)"
            if self.auto_cleanup:
                warning += "\n   → Attempting auto-cleanup..."
            return True, warning
        return False, ""
    
    def cleanup_temp_files(self) -> int:
        count = 0
        for temp_file in self.output_dir.rglob("temp.py"):
            try:
                temp_file.unlink()
                count += 1
            except:
                pass
        for pycache in self.output_dir.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache)
                count += 1
            except:
                pass
        if count > 0:
            self.cleanups += 1
        return count
    
    def check_and_cleanup(self) -> Tuple[bool, str]:
        is_low, warning = self.check_space()
        if not is_low:
            return False, ""
        if self.auto_cleanup:
            cleaned = self.cleanup_temp_files()
            total, used, free = self.get_disk_usage()
            message = f"{warning}\n   Cleaned {cleaned} files → {free:.2f} GB free"
            if free < self.min_free_gb:
                message += "\n   ❌ CRITICAL: Still low after cleanup!"
                return True, message
            message += "\n   ✅ Cleanup successful"
            return False, message
        return True, warning
    
    def get_status(self) -> str:
        total, used, free = self.get_disk_usage()
        return f"{free:.2f} GB free ({used/total*100:.1f}% used)"


class OutlierFilter:
    """异常参数过滤 - 防止 OOM"""
    def __init__(self, max_elements: int = int(1e8), max_memory_gb: float = 4.0):
        self.max_elements = max_elements
        self.max_memory_gb = max_memory_gb
        self.total_checks = 0
        self.filtered_count = 0
    
    def check_tensor_arg(self, arg) -> Tuple[bool, Optional[str]]:
        if not hasattr(arg, 'type') or arg.type != ArgType.TORCH_TENSOR:
            return False, None
        if not hasattr(arg, 'shape') or not arg.shape:
            return False, None
        
        num_elements = 1
        for dim in arg.shape:
            num_elements *= dim
        
        if num_elements > self.max_elements:
            return True, f"Too many elements: {num_elements:,} > {self.max_elements:,}"
        
        return False, None
    
    def check_api(self, api) -> Tuple[bool, Optional[str]]:
        self.total_checks += 1
        for param_name, arg in api.args.items():
            if arg is None:
                continue
            if hasattr(arg, 'type') and arg.type in [ArgType.LIST, ArgType.TUPLE]:
                if hasattr(arg, 'value') and arg.value:
                    for sub_arg in arg.value:
                        should_filter, reason = self.check_tensor_arg(sub_arg)
                        if should_filter:
                            self.filtered_count += 1
                            return True, f"{param_name}: {reason}"
            else:
                should_filter, reason = self.check_tensor_arg(arg)
                if should_filter:
                    self.filtered_count += 1
                    return True, f"{param_name}: {reason}"
        return False, None
    
    def get_status(self) -> str:
        rate = (self.filtered_count / self.total_checks * 100) if self.total_checks > 0 else 0
        return f"{self.filtered_count}/{self.total_checks} filtered ({rate:.1f}%)"


# =============================================================================
# Checkpoint System (断点续传)
# =============================================================================

class CheckpointManager:
    """检查点管理器 - 支持断点续传"""
    
    def __init__(self, checkpoint_dir: str, strategy: str, api_name: str):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        self.strategy = strategy
        self.api_name = api_name.replace('.', '_').replace('::', '_')
        
        self.checkpoint_file = self.checkpoint_dir / f"{self.api_name}_{strategy}_checkpoint.pkl"
        self.metadata_file = self.checkpoint_dir / f"{self.api_name}_{strategy}_metadata.json"
        
        print(f"[Checkpoint] Manager initialized: {self.checkpoint_file.name}")
    
    def save(self, iteration: int, coverage_kernels: set, 
             corpus_seeds: list = None, logger_iterations: int = 0) -> bool:
        try:
            checkpoint_data = {
                'iteration': iteration,
                'coverage_kernels': coverage_kernels,
                'corpus_seeds': corpus_seeds,
                'logger_iterations': logger_iterations,
                'strategy': self.strategy,
                'api_name': self.api_name
            }
            
            temp_file = self.checkpoint_file.with_suffix('.tmp')
            with open(temp_file, 'wb') as f:
                pickle.dump(checkpoint_data, f)
            
            temp_file.replace(self.checkpoint_file)
            
            metadata = {
                'iteration': iteration,
                'total_kernels': len(coverage_kernels),
                'corpus_size': len(corpus_seeds) if corpus_seeds else 0,
                'logger_iterations': logger_iterations,
                'strategy': self.strategy
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"[Checkpoint] ❌ Save failed: {e}")
            return False
    
    def load(self) -> Optional[Dict]:
        if not self.checkpoint_file.exists():
            return None
        
        try:
            with open(self.checkpoint_file, 'rb') as f:
                data = pickle.load(f)
            
            print(f"[Checkpoint] ✅ Loaded from iteration {data['iteration']}")
            print(f"  Kernels: {len(data['coverage_kernels'])}")
            if data.get('corpus_seeds'):
                print(f"  Corpus: {len(data['corpus_seeds'])} seeds")
            
            return data
            
        except Exception as e:
            print(f"[Checkpoint] ❌ Load failed: {e}")
            return None
    
    def exists(self) -> bool:
        return self.checkpoint_file.exists()
    
    def clear(self):
        try:
            if self.checkpoint_file.exists():
                self.checkpoint_file.unlink()
            if self.metadata_file.exists():
                self.metadata_file.unlink()
            print(f"[Checkpoint] Cleared")
        except:
            pass


# =============================================================================
# Feature Extractor (参数指纹提取)
# =============================================================================

def extract_features(api: TorchAPI) -> str:
    """
    提取 API 调用的参数指纹，用于后续的特征多样性分析
    
    返回格式: "param1:type1:value1|param2:type2:value2|..."
    """
    features = []
    
    for param_name, arg in api.args.items():
        if arg is None:
            continue
        
        if arg.type == ArgType.INT:
            features.append(f"{param_name}:int:{arg.value}")
        
        elif arg.type == ArgType.FLOAT:
            features.append(f"{param_name}:float:{arg.value:.2f}")
        
        elif arg.type == ArgType.BOOL:
            features.append(f"{param_name}:bool:{arg.value}")
        
        elif arg.type == ArgType.STR:
            features.append(f"{param_name}:str:{arg.value}")
        
        elif arg.type == ArgType.TORCH_DTYPE:
            dtype_str = str(arg.value).split(".")[-1] if hasattr(arg, 'value') else 'unknown'
            features.append(f"{param_name}:dtype:{dtype_str}")
        
        elif arg.type == ArgType.TORCH_TENSOR:
            shape_str = str(arg.shape) if hasattr(arg, 'shape') else 'unknown'
            dtype_str = str(arg.dtype).split(".")[-1] if hasattr(arg, 'dtype') else 'unknown'
            features.append(f"{param_name}:tensor:shape{shape_str}:dtype{dtype_str}")
        
        elif arg.type in [ArgType.LIST, ArgType.TUPLE]:
            length = len(arg.value) if hasattr(arg, 'value') and arg.value else 0
            type_name = "list" if arg.type == ArgType.LIST else "tuple"
            features.append(f"{param_name}:{type_name}:len{length}")
        
        else:
            features.append(f"{param_name}:{arg.type.name}:other")
    
    features.sort()
    return "|".join(features)


# =============================================================================
# Experiment Logger (原始数据记录器)
# =============================================================================

class ExperimentLogger:
    """轻量级实验数据记录器"""
    
    def __init__(self, output_file: str, strategy: str):
        self.output_file = output_file
        self.strategy = strategy
        self.file_handle = open(output_file, 'w', buffering=1)
        
        self.total_iterations = 0
        self.valid_count = 0
        self.invalid_count = 0
    
    def log_iteration(self, 
                     iteration: int,
                     source: str,
                     api: TorchAPI,
                     valid: bool,
                     kernels: List[str]):
        features = extract_features(api)
        
        record = {
            "iteration": iteration,
            "strategy": self.strategy,
            "source": source,
            "valid": valid,
            "features": features,
            "kernels": list(kernels) if kernels else []
        }
        
        self.file_handle.write(json.dumps(record) + '\n')
        
        self.total_iterations += 1
        if valid:
            self.valid_count += 1
        else:
            self.invalid_count += 1
    
    def get_valid_rate(self) -> float:
        if self.total_iterations == 0:
            return 0.0
        return self.valid_count / self.total_iterations
    
    def close(self):
        if self.file_handle:
            self.file_handle.close()
    
    def __del__(self):
        self.close()

# 保存原始方法
_ORIGINAL_DO_SELECT_FROM_DB = None
_ORIGINAL_MUTATE_INT_VALUE = None
_ORIGINAL_MUTATE_FLOAT_VALUE = None


# =============================================================================
# Bug Tracker (Bug 追踪器)
# =============================================================================

class BugTracker:
    """追踪所有类型的 Bug"""
    
    def __init__(self, name: str, output_dir: str):
        self.name = name
        self.output_dir = output_dir
        
        self.bugs = {
            "crash": [],
            "cuda": [],
            "precision": []
        }
        
        self.bug_files = {
            "crash": set(),
            "cuda": set(),
            "precision": set()
        }
    
    def scan_bugs(self):
        oracle_names = {
            "crash": "crash-oracle",
            "cuda": "cuda-oracle",
            "precision": "precision-oracle"
        }
        
        for bug_type, oracle_name in oracle_names.items():
            bug_dir = join(self.output_dir, oracle_name, "potential-bug")
            if os.path.exists(bug_dir):
                for root, dirs, files in os.walk(bug_dir):
                    for file in files:
                        if file.endswith('.py'):
                            bug_file = join(root, file)
                            if bug_file not in self.bug_files[bug_type]:
                                self.bug_files[bug_type].add(bug_file)
                                
                                api_name = os.path.basename(os.path.dirname(bug_file))
                                
                                self.bugs[bug_type].append((
                                    len(self.bugs[bug_type]),
                                    api_name,
                                    bug_file
                                ))
    
    def get_total_bugs(self) -> int:
        return sum(len(bugs) for bugs in self.bugs.values())
    
    def get_bugs_by_type(self, bug_type: str) -> int:
        return len(self.bugs.get(bug_type, []))
    
    def print_summary(self):
        print(f"\n{'='*70}")
        print(f"BUG DETECTION SUMMARY: {self.name}")
        print(f"{'='*70}")
        print(f"Total Bugs Found:    {self.get_total_bugs()}")
        print(f"  🔥 CRASH:          {self.get_bugs_by_type('crash')}")
        print(f"  🔀 CUDA:           {self.get_bugs_by_type('cuda')}")
        print(f"  ⚡ PRECISION:      {self.get_bugs_by_type('precision')}")
        print(f"{'='*70}")
        
        for bug_type in ["crash", "cuda", "precision"]:
            if self.bugs[bug_type]:
                print(f"\n{bug_type.upper()} Bugs (showing first 3):")
                for i, (bug_num, api_name, bug_file) in enumerate(self.bugs[bug_type][:3]):
                    rel_path = bug_file.replace(self.output_dir + "/", "")
                    print(f"  #{bug_num+1}: {api_name} -> {rel_path}")
                
                if len(self.bugs[bug_type]) > 3:
                    print(f"  ... and {len(self.bugs[bug_type]) - 3} more")


# =============================================================================
# 🔥 NEW: Adaptive Saturation Detector (动态饱和检测器)
# =============================================================================

class AdaptiveSaturationDetector:
    """
    动态饱和检测器 - 不停止，而是扩大搜索范围
    
    策略:
    1. 连续 N 次无发现 → 触发"扩大搜索"而非"停止"
    2. 扩大搜索 = 提升探索率 + 扩大变异范围
    3. 发现新 Kernel → 立即恢复正常模式
    """
    
    def __init__(self, 
                 patience: int = 500,           # 🔧 容忍多少次无新发现
                 check_interval: int = 100):
        self.patience = patience
        self.check_interval = check_interval
        
        self.no_discovery_count = 0
        self.last_kernel_count = 0
        self.last_check_iteration = 0
        
        # 扩大搜索标志
        self.expansion_mode = False
        self.expansion_count = 0
    
    def update(self, current_kernels: int, iteration: int) -> Tuple[bool, str]:
        """
        更新状态并检查是否需要扩大搜索
        
        Returns:
            (should_expand, message)
        """
        # 检查是否有新发现
        if current_kernels > self.last_kernel_count:
            self.no_discovery_count = 0
            self.last_kernel_count = current_kernels
            
            # 发现新 Kernel，退出扩展模式
            if self.expansion_mode:
                self.expansion_mode = False
                return False, "✅ New kernels found! Returning to normal mode"
        else:
            self.no_discovery_count += 1
        
        # 定期检查
        if iteration - self.last_check_iteration >= self.check_interval:
            self.last_check_iteration = iteration
            
            # 触发扩大搜索
            if self.no_discovery_count >= self.patience and not self.expansion_mode:
                self.expansion_mode = True
                self.expansion_count += 1
                return True, f"🔍 Expanding search (stagnation: {self.no_discovery_count} iters)"
        
        return False, ""
    
    def is_in_expansion_mode(self) -> bool:
        return self.expansion_mode
    
    def reset(self):
        self.no_discovery_count = 0
        self.expansion_mode = False


# =============================================================================
# Enhanced Coverage Tracker
# =============================================================================

class EnhancedCoverageTracker:
    """覆盖率追踪器 + 动态饱和检测"""
    
    def __init__(self, name: str, enable_adaptive_saturation: bool = True):
        self.name = name
        self.all_kernels: Set[str] = set()
        self.kernel_provenance: Dict[str, int] = {}
        self.history: List[Tuple[int, int]] = []
        self.new_kernel_iterations: List[int] = []
        
        # 动态饱和检测
        self.saturation_detector = AdaptiveSaturationDetector() if enable_adaptive_saturation else None
    
    def update(self, new_kernels: Set[str], iteration: int) -> Tuple[int, Tuple[bool, str]]:
        """
        更新覆盖率
        
        Returns:
            (new_kernel_count, (should_expand, message))
        """
        if not isinstance(new_kernels, set):
            new_kernels = set(new_kernels) if new_kernels else set()
        
        fresh = new_kernels - self.all_kernels
        
        if fresh:
            for kernel in fresh:
                self.kernel_provenance[kernel] = iteration
            
            self.all_kernels.update(fresh)
            self.new_kernel_iterations.append(iteration)
            
            print(f"  [{self.name}] Iter {iteration}: +{len(fresh)} new kernels! "
                  f"Total: {len(self.all_kernels)}")
            
            num_fresh = len(fresh)
        else:
            num_fresh = 0
        
        self.history.append((iteration, len(self.all_kernels)))
        
        # 动态饱和检测
        expansion_signal = (False, "")
        if self.saturation_detector:
            expansion_signal = self.saturation_detector.update(len(self.all_kernels), iteration)
            if expansion_signal[0]:
                print(f"\n{expansion_signal[1]}")
        
        return num_fresh, expansion_signal
    
    def get_total(self) -> int:
        return len(self.all_kernels)
    
    def get_exclusive(self, other: 'EnhancedCoverageTracker') -> Set[str]:
        return self.all_kernels - other.all_kernels
    
    def get_overlap(self, other: 'EnhancedCoverageTracker') -> Set[str]:
        return self.all_kernels & other.all_kernels


# =============================================================================
# Evolutionary Corpus
# =============================================================================

class EvolutionaryCorpus:
    """进化种子池"""
    
    def __init__(self, max_size: int = 100):
        self.corpus: List[TorchAPI] = []
        self.max_size = max_size
    
    def add_seed(self, api: TorchAPI, discovered_kernels: Set[str]):
        if len(discovered_kernels) == 0:
            return
        
        seed_copy = copy.deepcopy(api)
        self.corpus.append(seed_copy)
        
        if len(self.corpus) > self.max_size:
            self.corpus.pop(0)
    
    def select_parent(self) -> Optional[TorchAPI]:
        if not self.corpus:
            return None
        return random.choice(self.corpus)
    
    def size(self) -> int:
        return len(self.corpus)


# =============================================================================
# 🔥 NEW: Adaptive Mutation Controller (动态变异控制器)
# =============================================================================

class AdaptiveMutationController:
    """
    动态变异控制器
    
    功能:
    1. 根据停滞情况自动调整变异范围
    2. 支持 ε-greedy 探索策略
    3. 发现新 Kernel 时立即恢复微创模式
    """
    
    def __init__(self, 
                 base_epsilon: float = 0.1,          # 基础探索率
                 expansion_epsilon: float = 0.3,     # 扩张模式探索率
                 surgical_range: int = 8,            # 微创范围
                 exploration_range: int = 64):       # 探索范围
        self.base_epsilon = base_epsilon
        self.expansion_epsilon = expansion_epsilon
        self.surgical_range = surgical_range
        self.exploration_range = exploration_range
        
        # 当前状态
        self.current_epsilon = base_epsilon
        self.current_range = surgical_range
        self.expansion_mode = False
        
        # 统计
        self.exploration_count = 0
        self.exploitation_count = 0
    
    def should_explore(self) -> bool:
        """决定本次迭代是否采用探索模式"""
        if random.random() < self.current_epsilon:
            self.exploration_count += 1
            return True
        else:
            self.exploitation_count += 1
            return False
    
    def enter_expansion_mode(self):
        """进入扩张模式（停滞时触发）"""
        self.expansion_mode = True
        self.current_epsilon = self.expansion_epsilon
        self.current_range = self.exploration_range
        print(f"  🔍 [Mutation] Expansion mode: ε={self.current_epsilon}, range=±{self.current_range}")
    
    def exit_expansion_mode(self):
        """退出扩张模式（发现新 Kernel 时）"""
        self.expansion_mode = False
        self.current_epsilon = self.base_epsilon
        self.current_range = self.surgical_range
        print(f"  ✅ [Mutation] Normal mode: ε={self.current_epsilon}, range=±{self.current_range}")
    
    def get_mutation_range(self) -> int:
        """获取当前变异范围"""
        return self.current_range
    
    def get_status(self) -> str:
        total = self.exploration_count + self.exploitation_count
        if total == 0:
            return "No mutations yet"
        explore_pct = self.exploration_count / total * 100
        return (f"Explore: {self.exploration_count}/{total} ({explore_pct:.1f}%) | "
                f"Mode: {'Expansion' if self.expansion_mode else 'Normal'} | "
                f"ε={self.current_epsilon:.2f}, range=±{self.current_range}")


# =============================================================================
# Probability Patcher
# =============================================================================

class ProbabilityPatcher:
    """将数据库采样概率从 20% 提升到 80%"""
    
    @staticmethod
    def patch_high_db_probability():
        import utils.probability as prob_module
        
        global _ORIGINAL_DO_SELECT_FROM_DB
        _ORIGINAL_DO_SELECT_FROM_DB = prob_module.do_select_from_db
        
        def high_db_select() -> bool:
            from numpy.random import rand
            return rand() < 0.5
        
        prob_module.do_select_from_db = high_db_select
        print("[Patch] ✅ Database sampling: 20% → 80%")
    
    @staticmethod
    def restore():
        if _ORIGINAL_DO_SELECT_FROM_DB:
            import utils.probability as prob_module
            prob_module.do_select_from_db = _ORIGINAL_DO_SELECT_FROM_DB
            print("[Patch] 🔄 Database sampling restored")


# =============================================================================
# 🧪 NEW: Poison Patcher (投毒补丁 - 独立于策略)
# =============================================================================

# 保存原始方法的全局变量
_POISON_ORIGINAL_FLOAT = None
_POISON_ORIGINAL_INT = None

class PoisonPatcher:
    """
    独立的投毒补丁 - 对 Random 和 Guided 都生效
    
    浮点投毒:
    - 5%:  Infinity (±∞)
    - 5%:  NaN
    - 10%: Extreme Values [1e20, -1e20, 1e-10, -1e-10]
    - 30%: 字典采样
    - 50%: 温和微调
    
    整数投毒:
    - 10%: 边界值 [0, -1, 1]
    - 10%: 极端值 [-999, 999, ±2^31]
    - 10%: 陷阱值 [-2, -3, 256, 512, 质数]
    - 30%: 字典采样
    - 40%: 温和微调
    """
    
    @staticmethod
    def patch():
        global _POISON_ORIGINAL_FLOAT, _POISON_ORIGINAL_INT
        
        _POISON_ORIGINAL_FLOAT = Argument.mutate_float_value
        _POISON_ORIGINAL_INT = Argument.mutate_int_value
        
        def poison_float_mutation(self, value) -> float:
            """🧪 Float Poison Injection - 对所有策略生效"""
            from numpy.random import rand, choice
            
            roll = rand()
            
            # [5%] 注入 Infinity (正/负无穷)
            if roll < 0.05:
                return choice([float('inf'), float('-inf')])
            
            # [5%] 注入 NaN
            elif roll < 0.10:
                return float('nan')
            
            # [10%] 注入极端值 (Extreme Values)
            elif roll < 0.20:
                extreme_values = [1e20, -1e20, 1e-10, -1e-10]
                return choice(extreme_values)
            
            # [30%] 原始逻辑 - 字典采样
            elif roll < 0.50:
                return choice(Argument._float_values)
            
            # [50%] 原始逻辑 - 温和微调
            else:
                return value + (rand() - 0.5) * 8.0
        
        def poison_int_mutation(self, value, _min=None, _max=None) -> int:
            """🧪 Int Poison Injection - 对所有策略生效"""
            from numpy.random import rand, choice, randint
            
            roll = rand()
            
            # [10%] 边界值 - 最容易触发逻辑错误
            if roll < 0.10:
                boundary_values = [0, -1, 1]
                new_value = choice(boundary_values)
            
            # [10%] 极端值 - 溢出和边界检查
            elif roll < 0.20:
                extreme_values = [-999, 999, -2147483648, 2147483647, -65536, 65536]
                new_value = choice(extreme_values)
            
            # [10%] 常见陷阱值 - 特定参数的问题值
            elif roll < 0.30:
                trap_values = [
                    -2, -3, -4,      # 负数维度
                    256, 512, 1024,  # 大尺寸
                    7, 11, 13,       # 质数 (不能整除)
                    0,               # 重复强调 0
                ]
                new_value = choice(trap_values)
            
            # [30%] 字典采样
            elif roll < 0.60:
                new_value = choice(Argument._int_values)
            
            # [40%] 温和微调
            else:
                new_value = value + randint(-8, 9)
            
            # 应用边界限制 (但保留 -1 等特殊值用于触发 bug)
            if _min is not None and new_value < _min and new_value not in [-1, 0]:
                new_value = max(_min, new_value)
            if _max is not None and new_value > _max:
                new_value = min(_max, new_value)
            
            return int(new_value)
        
        Argument.mutate_float_value = poison_float_mutation
        Argument.mutate_int_value = poison_int_mutation
        print("[Patch] 🧪 Poison Injection enabled (ALL strategies):")
        print("        Float: 5% Inf + 5% NaN + 10% Extreme")
        print("        Int:   10% boundary + 10% extreme + 10% trap")
    
    @staticmethod
    def restore():
        global _POISON_ORIGINAL_FLOAT, _POISON_ORIGINAL_INT
        if _POISON_ORIGINAL_FLOAT:
            Argument.mutate_float_value = _POISON_ORIGINAL_FLOAT
        if _POISON_ORIGINAL_INT:
            Argument.mutate_int_value = _POISON_ORIGINAL_INT
        print("[Patch] 🔄 Poison Injection restored")


# =============================================================================
# 🔥 NEW: Adaptive Mutation Patcher (动态变异补丁 - 仅 Guided)
# =============================================================================

class AdaptiveMutationPatcher:
    """动态范围变异补丁 - 仅 Guided 策略使用，投毒由 PoisonPatcher 统一处理"""
    
    @staticmethod
    def patch_adaptive_mutation(controller: AdaptiveMutationController):
        """
        Guided 策略额外使用动态范围调整
        注意: 基础投毒已由 PoisonPatcher 处理，这里只增加动态范围功能
        """
        # 注意: 不再保存/覆盖原始方法，因为 PoisonPatcher 已经处理了
        # 这个 patcher 现在只是一个标记，表示 Guided 策略启用了动态范围
        print(f"[Patch] ✅ Adaptive range enabled for Guided: ±{controller.get_mutation_range()}")
    
    @staticmethod
    def restore():
        # PoisonPatcher 会负责恢复，这里只打印信息
        print("[Patch] 🔄 Adaptive range disabled")


# =============================================================================
# 🔥 Enhanced Fuzzer with Hybrid Strategy
# =============================================================================

class EnhancedFuzzer:
    """支持混合策略的增强型 Fuzzer"""
    
    def __init__(self, 
                 api_name: str, 
                 output_dir: str, 
                 strategy_name: str, 
                 enable_patches: bool,
                 use_all_oracles: bool = True,
                 enable_logging: bool = True,
                 enable_checkpoint: bool = True,
                 enable_safety_guards: bool = True,
                 diff_bound: float = 1e-5):  # 🔧
        self.api_name = api_name
        self.output_dir = output_dir
        self.strategy_name = strategy_name
        self.enable_patches = enable_patches
        self.use_all_oracles = use_all_oracles
        self.enable_logging = enable_logging
        self.enable_checkpoint = enable_checkpoint
        self.enable_safety_guards = enable_safety_guards
        self.diff_bound = diff_bound
        
        # Trackers
        self.coverage = EnhancedCoverageTracker(strategy_name, enable_adaptive_saturation=enable_patches)
        self.bug_tracker = BugTracker(strategy_name, output_dir)
        
        # Guided 专属
        self.corpus = EvolutionaryCorpus(max_size=100) if enable_patches else None
        self.mutation_controller = AdaptiveMutationController() if enable_patches else None
        
        # Library - 使用更严格的 diff_bound 配合投毒策略
        self.library = TorchLibrary(output_dir, diff_bound=diff_bound)
        print(f"[Fuzzer] 🎯 Precision tolerance: diff_bound={diff_bound}")
        
        # Oracle 列表
        if use_all_oracles:
            self.oracles = [OracleType.CRASH, OracleType.CUDA, OracleType.PRECISION]
            print(f"[Fuzzer] Using ALL oracles: CRASH + CUDA + PRECISION")
        else:
            self.oracles = [OracleType.CRASH]
            print(f"[Fuzzer] Using CRASH oracle only")
        
        # Experiment Logger
        self.logger = None
        if enable_logging:
            api_clean = api_name.replace('.', '_').replace('::', '_')
            log_file = join(output_dir, f"{api_clean}_{strategy_name.lower()}_trace.jsonl")
            self.logger = ExperimentLogger(log_file, strategy_name.lower())
            print(f"[Logger] Trace file: {log_file}")
        
        # Checkpoint Manager
        self.checkpoint_manager = None
        if enable_checkpoint:
            self.checkpoint_manager = CheckpointManager(
                checkpoint_dir=output_dir,
                strategy=strategy_name.lower(),
                api_name=api_name
            )
        
        # Safety Guards
        self.speedometer = None
        self.disk_guard = None
        self.outlier_filter = None
        
        if enable_safety_guards:
            self.speedometer = Speedometer(window_size=100, slow_threshold=0.5)
            self.disk_guard = DiskGuard(output_dir, min_free_gb=1.0, auto_cleanup=True)
            self.outlier_filter = OutlierFilter(max_elements=int(1e8), max_memory_gb=4.0)
            print(f"[Safety] Guards enabled: Speedometer + DiskGuard + OutlierFilter")
        
        print(f"\n[Fuzzer] Initialized: {strategy_name}")
        print(f"  API: {api_name}")
        print(f"  Patches: {'Enabled' if enable_patches else 'Disabled'}")
        print(f"  Hybrid Strategy: {'Active' if self.mutation_controller else 'N/A'}")
        print(f"  Data Logging: {'Enabled' if enable_logging else 'Disabled'}")
        print(f"  Checkpoint: {'Enabled' if enable_checkpoint else 'Disabled'}")
        print(f"  Safety Guards: {'Enabled' if enable_safety_guards else 'Disabled'}")
    
    def run_fuzzing_loop(self, 
                        max_iterations: int = 10000,
                        checkpoint_interval: int = 100,
                        bug_scan_interval: int = 50):
        """
        主 Fuzzing 循环 - 混合策略版本
        """
        # ====================================================================
        # 初始化 Safety Guards
        # ====================================================================
        if self.speedometer:
            self.speedometer.start()
        
        # ====================================================================
        # 尝试从 checkpoint 恢复
        # ====================================================================
        start_iteration = 0
        
        if self.checkpoint_manager and self.checkpoint_manager.exists():
            print(f"\n{'='*70}")
            print(f"CHECKPOINT DETECTED")
            print(f"{'='*70}")
            
            checkpoint_data = self.checkpoint_manager.load()
            
            if checkpoint_data:
                self.coverage.all_kernels = checkpoint_data['coverage_kernels']
                self.coverage.history = [(checkpoint_data['iteration'], len(checkpoint_data['coverage_kernels']))]
                
                if self.corpus and checkpoint_data.get('corpus_seeds'):
                    self.corpus.corpus = checkpoint_data['corpus_seeds']
                
                start_iteration = checkpoint_data['iteration'] + 1
                
                if self.logger:
                    self.logger.total_iterations = checkpoint_data.get('logger_iterations', 0)
                
                print(f"\n✅ Resuming from iteration {start_iteration}")
                print(f"  Previous kernels: {len(self.coverage.all_kernels)}")
                if self.corpus:
                    print(f"  Previous corpus: {len(self.corpus.corpus)} seeds")
                print(f"{'='*70}\n")
        
        # ====================================================================
        # 主循环
        # ====================================================================
        print(f"\n{'='*70}")
        print(f"Starting {self.strategy_name} fuzzing")
        if self.mutation_controller:
            print(f"Hybrid Strategy: ε-greedy + Adaptive Mutation")
        print(f"Iterations: {start_iteration} → {max_iterations}")
        if start_iteration > 0:
            print(f"(Resuming from checkpoint)")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        last_bug_count = 0
        
        for i in range(start_iteration, max_iterations):
            # ================================================================
            # Speedometer tick
            # ================================================================
            if self.speedometer:
                self.speedometer.tick()
            
            # ================================================================
            # 🔥 混合策略：ε-greedy 选择
            # ================================================================
            source = ""
            is_exploration = False
            
            if self.mutation_controller:
                is_exploration = self.mutation_controller.should_explore()
            
            if is_exploration:
                # 探索模式：强制随机种子 + 大范围变异
                api = TorchAPI(self.api_name)
                source = "exploration"
            else:
                # 利用模式：优先使用 Corpus
                if self.corpus and self.corpus.size() > 0 and random.random() < 0.7:
                    parent_api = self.corpus.select_parent()
                    api = copy.deepcopy(parent_api)
                    source = "corpus"
                else:
                    api = TorchAPI(self.api_name)
                    source = "random"
            
            # 变异
            api.mutate()
            
            # ================================================================
            # OutlierFilter 检查
            # ================================================================
            if self.outlier_filter:
                should_filter, reason = self.outlier_filter.check_api(api)
                if should_filter:
                    if self.logger:
                        self.logger.log_iteration(
                            iteration=i,
                            source=source,
                            api=api,
                            valid=False,
                            kernels=[]
                        )
                    continue
            
            # ================================================================
            # 测试所有 Oracle
            # ================================================================
            all_captured_kernels = set()
            execution_valid = False
            
            for oracle in self.oracles:
                try:
                    captured_kernels = self.library.test_with_oracle(api, oracle)
                    all_captured_kernels.update(captured_kernels)
                    execution_valid = True
                except Exception as e:
                    pass
            
            # 记录原始数据
            if self.logger:
                self.logger.log_iteration(
                    iteration=i,
                    source=source,
                    api=api,
                    valid=execution_valid,
                    kernels=list(all_captured_kernels)
                )
            
            # ================================================================
            # 更新覆盖率 + 动态饱和检测
            # ================================================================
            new_count, (should_expand, expansion_msg) = self.coverage.update(all_captured_kernels, i)
            
            # 响应扩张信号
            if should_expand and self.mutation_controller:
                self.mutation_controller.enter_expansion_mode()
            
            # 发现新 Kernel 时退出扩张模式
            if new_count > 0 and self.mutation_controller:
                if self.mutation_controller.expansion_mode:
                    self.mutation_controller.exit_expansion_mode()
            
            # 更新 Corpus
            if new_count > 0 and self.corpus:
                self.corpus.add_seed(api, all_captured_kernels)
            
            # 定期扫描 Bug
            if (i + 1) % bug_scan_interval == 0:
                prev_bug_count = self.bug_tracker.get_total_bugs()
                self.bug_tracker.scan_bugs()
                new_bugs = self.bug_tracker.get_total_bugs() - prev_bug_count
                
                if new_bugs > 0:
                    print(f"  🐛 [{self.strategy_name}] Found {new_bugs} new bugs! "
                          f"Total: {self.bug_tracker.get_total_bugs()}")
            
            # ================================================================
            # Checkpoint + Safety Guards
            # ================================================================
            if (i + 1) % checkpoint_interval == 0:
                # Checkpoint 保存
                if self.checkpoint_manager:
                    self.checkpoint_manager.save(
                        iteration=i,
                        coverage_kernels=self.coverage.all_kernels,
                        corpus_seeds=self.corpus.corpus if self.corpus else None,
                        logger_iterations=self.logger.total_iterations if self.logger else 0
                    )
                
                # 磁盘空间检查
                if self.disk_guard:
                    is_critical, message = self.disk_guard.check_and_cleanup()
                    if is_critical:
                        print(f"\n{message}")
                        print(f"❌ STOPPING: Critical disk space issue")
                        break
                    elif message:
                        print(f"\n{message}")
                
                # Progress Checkpoint
                elapsed = time.time() - start_time
                valid_rate_str = ""
                if self.logger:
                    valid_rate_str = f" | Valid: {self.logger.get_valid_rate()*100:.1f}%"
                
                print(f"\n--- Checkpoint: {i+1}/{max_iterations} ({elapsed/60:.1f} min) ---")
                print(f"Kernels: {self.coverage.get_total()} | "
                      f"Bugs: {self.bug_tracker.get_total_bugs()}{valid_rate_str}")
                
                # Speedometer 状态
                if self.speedometer:
                    print(f"Speed: {self.speedometer.get_status(i, max_iterations)}")
                    is_slow, warning = self.speedometer.check_speed()
                    if is_slow:
                        print(warning)
                
                # Disk 状态
                if self.disk_guard:
                    print(f"Disk: {self.disk_guard.get_status()}")
                
                # OutlierFilter 状态
                if self.outlier_filter:
                    print(f"Filter: {self.outlier_filter.get_status()}")
                
                # Corpus 状态
                if self.corpus:
                    print(f"Corpus: {self.corpus.size()} seeds")
                
                # 🔥 Mutation Controller 状态
                if self.mutation_controller:
                    print(f"Mutation: {self.mutation_controller.get_status()}")
                
                # Bug 扫描
                self.bug_tracker.scan_bugs()
        
        # ====================================================================
        # 完成后清理
        # ====================================================================
        if self.checkpoint_manager:
            self.checkpoint_manager.clear()
        
        # 最终统计
        print(f"\n{'='*70}")
        print(f"Fuzzing completed: {self.strategy_name}")
        print(f"Total time: {(time.time() - start_time)/60:.1f} minutes")
        
        if self.logger:
            print(f"Valid Rate: {self.logger.get_valid_rate()*100:.1f}%")
            print(f"Trace file: {self.logger.output_file}")
            self.logger.close()
        
        if self.speedometer:
            print(f"Average Speed: {self.speedometer.get_average_speed():.2f} it/s")
            if self.speedometer.slow_warnings > 0:
                print(f"Slow Warnings: {self.speedometer.slow_warnings}")
        
        if self.disk_guard:
            total, used, free = self.disk_guard.get_disk_usage()
            print(f"Final Disk Usage: {free:.2f} GB free")
            if self.disk_guard.cleanups > 0:
                print(f"Cleanups Performed: {self.disk_guard.cleanups}")
        
        if self.outlier_filter:
            print(f"Outliers Filtered: {self.outlier_filter.filtered_count}/{self.outlier_filter.total_checks}")
        
        if self.mutation_controller:
            print(f"Mutation Stats: {self.mutation_controller.get_status()}")
        
        print(f"{'='*70}")
        
        return self.coverage
    
    def print_stats(self):
        """打印统计信息"""
        print(f"\n{'='*70}")
        print(f"FINAL STATISTICS: {self.strategy_name}")
        print(f"{'='*70}")
        print(f"Total Kernels: {self.coverage.get_total()}")
        
        # Bug 统计
        self.bug_tracker.scan_bugs()
        self.bug_tracker.print_summary()


# =============================================================================
# Visualization
# =============================================================================

def plot_full_oracle_results(
    random_coverage: EnhancedCoverageTracker,
    guided_coverage: EnhancedCoverageTracker,
    random_bugs: BugTracker,
    guided_bugs: BugTracker,
    api_name: str,
    output_dir: str
):
    """绘制完整的结果对比图（包含 Bug 统计）"""
    
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # Kernel 覆盖率曲线
    ax1 = fig.add_subplot(gs[0, :2])
    
    if random_coverage.history:
        iters, kernels = zip(*random_coverage.history)
        ax1.plot(iters, kernels, 
                label=f"Random (Total: {random_coverage.get_total()})",
                color="#3498db", linewidth=3, alpha=0.8)
    
    if guided_coverage.history:
        iters, kernels = zip(*guided_coverage.history)
        ax1.plot(iters, kernels,
                label=f"Guided (Total: {guided_coverage.get_total()})",
                color="#e74c3c", linewidth=3)
    
    ax1.set_xlabel("Iteration", fontsize=12)
    ax1.set_ylabel("Cumulative Kernels", fontsize=12)
    ax1.set_title("A) Kernel Coverage Over Time (Hybrid Strategy)", 
                  fontsize=13, fontweight='bold')
    ax1.legend(loc="lower right", fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Bug 数量对比
    ax2 = fig.add_subplot(gs[0, 2])
    
    bug_types = ['CRASH', 'CUDA', 'PRECISION']
    random_bug_counts = [
        random_bugs.get_bugs_by_type('crash'),
        random_bugs.get_bugs_by_type('cuda'),
        random_bugs.get_bugs_by_type('precision')
    ]
    guided_bug_counts = [
        guided_bugs.get_bugs_by_type('crash'),
        guided_bugs.get_bugs_by_type('cuda'),
        guided_bugs.get_bugs_by_type('precision')
    ]
    
    x = np.arange(len(bug_types))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, random_bug_counts, width, 
                    label='Random', color='#3498db', alpha=0.8)
    bars2 = ax2.bar(x + width/2, guided_bug_counts, width,
                    label='Guided', color='#e74c3c', alpha=0.8)
    
    ax2.set_xlabel("Bug Type", fontsize=11)
    ax2.set_ylabel("Count", fontsize=11)
    ax2.set_title("B) Bugs Found by Type", fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(bug_types)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=9)
    
    # 总 Bug 数对比
    ax3 = fig.add_subplot(gs[1, 0])
    
    total_random = random_bugs.get_total_bugs()
    total_guided = guided_bugs.get_total_bugs()
    
    if total_random > 0 or total_guided > 0:
        sizes = [total_random, total_guided]
        labels = [f'Random\n({total_random})', f'Guided\n({total_guided})']
        colors = ['#3498db', '#e74c3c']
        explode = (0.05, 0.05)
        
        ax3.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90,
                textprops={'fontsize': 11, 'weight': 'bold'})
        ax3.set_title("C) Total Bugs Distribution", 
                     fontsize=12, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, "No Bugs Found", 
                ha='center', va='center', fontsize=14)
        ax3.axis('off')
    
    # 发现速率
    ax4 = fig.add_subplot(gs[1, 1])
    
    window = 100
    random_rates = []
    guided_rates = []
    
    for i in range(window, len(random_coverage.history), window):
        prev_k = random_coverage.history[i-window][1]
        curr_k = random_coverage.history[i][1]
        rate = (curr_k - prev_k) / window
        random_rates.append((random_coverage.history[i][0], rate))
    
    for i in range(window, len(guided_coverage.history), window):
        prev_k = guided_coverage.history[i-window][1]
        curr_k = guided_coverage.history[i][1]
        rate = (curr_k - prev_k) / window
        guided_rates.append((guided_coverage.history[i][0], rate))
    
    if random_rates:
        iters, rates = zip(*random_rates)
        ax4.plot(iters, rates, label="Random", 
                color="#3498db", linewidth=2, marker='o', markersize=3)
    
    if guided_rates:
        iters, rates = zip(*guided_rates)
        ax4.plot(iters, rates, label="Guided", 
                color="#e74c3c", linewidth=2, marker='s', markersize=3)
    
    ax4.set_xlabel("Iteration", fontsize=11)
    ax4.set_ylabel(f"Rate (kernels/{window} iters)", fontsize=11)
    ax4.set_title("D) Kernel Discovery Rate", 
                  fontsize=12, fontweight='bold')
    ax4.legend(loc="upper right", fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # 统计表
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.axis('off')
    
    table_data = [
        ["Metric", "Random", "Guided", "Ratio"],
        ["", "", "", ""],
        ["Kernels", 
         f"{random_coverage.get_total()}",
         f"{guided_coverage.get_total()}",
         f"{guided_coverage.get_total()/max(random_coverage.get_total(),1):.2f}x"],
        ["Total Bugs",
         f"{random_bugs.get_total_bugs()}",
         f"{guided_bugs.get_total_bugs()}",
         f"{guided_bugs.get_total_bugs()/max(random_bugs.get_total_bugs(),1):.2f}x"],
        ["CRASH Bugs",
         f"{random_bugs.get_bugs_by_type('crash')}",
         f"{guided_bugs.get_bugs_by_type('crash')}",
         f"{guided_bugs.get_bugs_by_type('crash')/max(random_bugs.get_bugs_by_type('crash'),1):.2f}x"],
        ["CUDA Bugs",
         f"{random_bugs.get_bugs_by_type('cuda')}",
         f"{guided_bugs.get_bugs_by_type('cuda')}",
         f"{guided_bugs.get_bugs_by_type('cuda')/max(random_bugs.get_bugs_by_type('cuda'),1):.2f}x"],
        ["PRECISION Bugs",
         f"{random_bugs.get_bugs_by_type('precision')}",
         f"{guided_bugs.get_bugs_by_type('precision')}",
         f"{guided_bugs.get_bugs_by_type('precision')/max(random_bugs.get_bugs_by_type('precision'),1):.2f}x"],
    ]
    
    table = ax5.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.35, 0.22, 0.22, 0.21])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.5)
    
    for i in range(4):
        table[(0, i)].set_facecolor('#34495e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(4):
        table[(1, i)].set_facecolor('#ecf0f1')
    
    ax5.set_title("E) Comprehensive Comparison", 
                  fontsize=12, fontweight='bold', pad=20)
    
    # 总标题
    fig.suptitle(
        f"Hybrid Strategy Benchmark: {api_name}\n"
        f"ε-greedy (10% Exploration) + Adaptive Mutation + Dynamic Saturation",
        fontsize=15, fontweight='bold', y=0.98
    )
    
    plt.tight_layout()
    
    plot_file = join(output_dir, f"{api_name.replace('.', '_')}_hybrid_strategy.png")
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n📊 Hybrid strategy plot saved: {plot_file}")


# =============================================================================
# Main Experiment Runner
# =============================================================================

def run_full_oracle_experiment(
    api_name: str,
    max_iterations: int,
    output_dir: str,
    config_file: str = "demo_torch.conf",
    diff_bound: float = 1e-5
):
    """运行完整的混合策略实验 (含投毒策略)"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 配置数据库
    config = configparser.ConfigParser()
    possible_paths = [
        join("config", config_file),
        join("..", "config", config_file),
        config_file,
    ]
    
    config_path = None
    for path in possible_paths:
        if os.path.exists(path):
            config_path = path
            break
    
    if not config_path:
        print("❌ Config file not found")
        return None
    
    print(f"📝 Config: {os.path.abspath(config_path)}")
    config.read(config_path)
    
    TorchDatabase.database_config(
        config["mongodb"]["host"],
        int(config["mongodb"]["port"]),
        config["mongodb"]["torch_database"]
    )
    
    # =========================================================================
    # Phase 1: Random Baseline
    # =========================================================================
    # =========================================================================
    # 🧪 Enable Poison Injection for ALL strategies
    # =========================================================================
    PoisonPatcher.patch()
    
    try:
        # =========================================================================
        # Phase 1: Random Baseline
        # =========================================================================
        print("\n" + "="*70)
        print("PHASE 1: RANDOM BASELINE (All Oracles + Poison)")
        print("="*70)
        
        random_fuzzer = EnhancedFuzzer(
            api_name=api_name,
            output_dir=join(output_dir, "random"),
            strategy_name="Random",
            enable_patches=False,
            use_all_oracles=True,
            diff_bound=diff_bound
        )
        
        random_coverage = random_fuzzer.run_fuzzing_loop(
            max_iterations=max_iterations,
            checkpoint_interval=max(100, max_iterations // 20),
            bug_scan_interval=50
        )
        random_fuzzer.print_stats()
        
        # =========================================================================
        # Phase 2: Guided Strategy with Hybrid Approach
        # =========================================================================
        print("\n" + "="*70)
        print("PHASE 2: KERNEL-GUIDED WITH HYBRID STRATEGY (+ Poison)")
        print("="*70)
        
        ProbabilityPatcher.patch_high_db_probability()
        
        guided_fuzzer = EnhancedFuzzer(
            api_name=api_name,
            output_dir=join(output_dir, "guided"),
            strategy_name="Guided",
            enable_patches=True,
            use_all_oracles=True,
            diff_bound=diff_bound
        )
        
        # 🔥 应用动态变异补丁 (仅 Guided)
        AdaptiveMutationPatcher.patch_adaptive_mutation(guided_fuzzer.mutation_controller)
        
        guided_coverage = guided_fuzzer.run_fuzzing_loop(
            max_iterations=max_iterations,
            checkpoint_interval=max(100, max_iterations // 20),
            bug_scan_interval=50
        )
        guided_fuzzer.print_stats()
        
    finally:
        # 恢复所有补丁
        ProbabilityPatcher.restore()
        AdaptiveMutationPatcher.restore()
        PoisonPatcher.restore()
    
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
        "hybrid_strategy": {
            "epsilon_greedy": "10% exploration",
            "adaptive_mutation": "±8 → ±64 on stagnation",
            "dynamic_saturation": "expand search instead of stop"
        },
        "random": {
            "total_kernels": random_coverage.get_total(),
            "iterations_run": len(random_coverage.history),
            "bugs": {
                "total": random_fuzzer.bug_tracker.get_total_bugs(),
                "crash": random_fuzzer.bug_tracker.get_bugs_by_type("crash"),
                "cuda": random_fuzzer.bug_tracker.get_bugs_by_type("cuda"),
                "precision": random_fuzzer.bug_tracker.get_bugs_by_type("precision")
            }
        },
        "guided": {
            "total_kernels": guided_coverage.get_total(),
            "iterations_run": len(guided_coverage.history),
            "bugs": {
                "total": guided_fuzzer.bug_tracker.get_total_bugs(),
                "crash": guided_fuzzer.bug_tracker.get_bugs_by_type("crash"),
                "cuda": guided_fuzzer.bug_tracker.get_bugs_by_type("cuda"),
                "precision": guided_fuzzer.bug_tracker.get_bugs_by_type("precision")
            }
        },
        "comparison": {
            "kernel_ratio": guided_coverage.get_total() / max(random_coverage.get_total(), 1),
            "bug_ratio": guided_fuzzer.bug_tracker.get_total_bugs() / max(random_fuzzer.bug_tracker.get_total_bugs(), 1),
            "exclusive_random": len(random_coverage.get_exclusive(guided_coverage)),
            "exclusive_guided": len(guided_coverage.get_exclusive(random_coverage))
        }
    }
    
    result_file = join(output_dir, f"{api_name.replace('.', '_')}_hybrid_results.json")
    with open(result_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved: {result_file}")
    
    return results


# =============================================================================
# Main
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Hybrid Strategy Benchmark: ε-greedy + Adaptive Mutation + Poison Injection"
    )
    parser.add_argument("--api", type=str, default="torch.nn.LSTM",
                       help="API to test")
    parser.add_argument("--max-iterations", type=int, default=10000,
                       help="Maximum iterations")
    parser.add_argument("--output", type=str, default="hybrid_output")
    parser.add_argument("--conf", type=str, default="demo_torch.conf")
    parser.add_argument("--diff-bound", type=float, default=1e-5,
                       help="Precision tolerance for PRECISION oracle (default: 1e-5)")
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔬 HYBRID STRATEGY BENCHMARK + POISON INJECTION")
    print("="*70)
    print(f"API: {args.api}")
    print(f"Max Iterations: {args.max_iterations:,}")
    print(f"Strategy: ε-greedy (10% exploration) + Adaptive Mutation")
    print(f"🧪 Poison Injection: 5% Inf + 5% NaN + 10% Extreme")
    print(f"🎯 Precision Tolerance: {args.diff_bound}")
    print(f"Oracles: CRASH + CUDA + PRECISION")
    print("="*70)
    
    run_full_oracle_experiment(
        api_name=args.api,
        max_iterations=args.max_iterations,
        output_dir=args.output,
        config_file=args.conf,
        diff_bound=args.diff_bound
    )


if __name__ == "__main__":
    main()