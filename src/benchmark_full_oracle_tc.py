"""
Kernel-Guided Fuzzing Benchmark - HKG (Hybrid Kernel-Guided) Edition
=====================================================================

核心增强:
1. **DispatcherSpace**: 基于 PyTorch Dispatcher 机制的状态覆盖率计算
   - 理论全集: Dtype × Layout × Device × MemoryFormat × ...
   - 实际覆盖: 运行时成功执行的参数组合
   - 覆盖率: Numerator / Denominator

2. **HKGFuzzEngine**: 混合热启动策略
   - Phase 1 (Warm-up): 前 warmup_ratio 迭代使用 Random 快速填充 Corpus
   - Phase 2 (Evolution): 切换到 Kernel-Guided 模式深度探索

3. **CSVLogger**: 流式日志写入，避免内存溢出

4. **保持兼容**: 与现有 EnhancedFuzzer 完全兼容

Author: Research Team
Date: 2025-12-28
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
import csv
import itertools
from os.path import join
from pathlib import Path
from typing import Set, List, Dict, Tuple, Optional, Any, FrozenSet
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
# DispatcherSpace (分发器状态空间) - 核心创新
# =============================================================================

class DispatcherSpace:
    """
    Dispatcher State Coverage Calculator
    =====================================
    
    基于 PyTorch Dispatcher 机制的状态覆盖率计算器。
    
    核心概念:
    ---------
    PyTorch 的 Dispatcher 根据输入张量的多个维度选择对应的 Kernel 实现:
    - dtype: 数据类型 (float32, int64, bool, etc.)
    - layout: 内存布局 (strided, sparse_coo, sparse_csr, etc.)
    - device: 设备类型 (cpu, cuda, etc.)
    - memory_format: 内存格式 (contiguous, channels_last, etc.)
    
    覆盖率计算公式:
    ----------------
    分母 (Denominator): 
        理论全集 = |dtype| × |layout| × |device| × |memory_format| × ...
        
    分子 (Numerator):
        实际成功执行的参数组合数量 (去重后)
        
    覆盖率 = Numerator / Denominator × 100%
    
    设计目标:
    ---------
    传统的代码行覆盖率 (Line Coverage) 对于深度学习框架测试并不可靠，因为:
    1. 同一行代码可能被不同的 dtype/device 组合触发
    2. Kernel 选择逻辑是运行时动态决定的
    
    Dispatcher State Coverage 通过量化参数组合的覆盖情况，
    能更准确地反映测试的"逻辑完备性"。
    
    Example:
    --------
    >>> space = DispatcherSpace()
    >>> space.register_api("torch.add", {
    ...     "dtype": ["float32", "float64", "int32", "int64"],
    ...     "device": ["cpu", "cuda"],
    ...     "layout": ["strided", "sparse_coo"]
    ... })
    >>> # 理论全集 = 4 × 2 × 2 = 16 种组合
    >>> space.record_hit("torch.add", {"dtype": "float32", "device": "cpu", "layout": "strided"})
    >>> print(space.get_coverage("torch.add"))  # 输出: 6.25% (1/16)
    """
    
    # PyTorch 支持的数据类型 (与 TorchArgument._dtypes 对应)
    DEFAULT_DTYPES = [
        "int8", "int16", "int32", "int64",
        "uint8",
        "float16", "float32", "float64", "bfloat16",
        "complex64", "complex128",
        "bool"
    ]
    
    # PyTorch 支持的内存布局
    DEFAULT_LAYOUTS = [
        "strided",        # 标准密集张量
        "sparse_coo",     # COO 稀疏格式
        "sparse_csr",     # CSR 稀疏格式
        # "sparse_csc",   # CSC (较新版本)
    ]
    
    # PyTorch 支持的设备类型
    DEFAULT_DEVICES = [
        "cpu",
        "cuda"
    ]
    
    # PyTorch 支持的内存格式
    DEFAULT_MEMORY_FORMATS = [
        "contiguous_format",
        "channels_last",
        "channels_last_3d",
        "preserve_format"
    ]
    
    def __init__(self, name: str = "default"):
        """
        初始化 DispatcherSpace
        
        Args:
            name: 空间名称，用于区分不同的测试场景
        """
        self.name = name
        
        # API -> 维度定义
        # 格式: {api_name: {"dtype": [...], "device": [...], ...}}
        self.api_dimensions: Dict[str, Dict[str, List[str]]] = {}
        
        # API -> 理论全集大小 (分母)
        # 格式: {api_name: int}
        self.api_denominator: Dict[str, int] = {}
        
        # API -> 已覆盖的状态组合 (分子，使用 frozenset 存储便于去重)
        # 格式: {api_name: Set[FrozenSet[Tuple[str, str]]]}
        # 每个组合表示为: frozenset({("dtype", "float32"), ("device", "cpu"), ...})
        self.api_hits: Dict[str, Set[FrozenSet[Tuple[str, str]]]] = defaultdict(set)
        
        # 全局统计
        self.total_record_calls = 0
        self.total_unique_hits = 0
        
        # 历史记录 (iteration, coverage_percentage)
        self.coverage_history: List[Tuple[int, float]] = []
        
    def register_api(self, api_name: str, dimensions: Optional[Dict[str, List[str]]] = None):
        """
        注册一个 API 并定义其状态空间维度
        
        Args:
            api_name: API 名称，如 "torch.add"
            dimensions: 维度定义，格式: {"dtype": [...], "device": [...], ...}
                        如果为 None，则使用默认维度
        
        计算公式:
            Denominator = |dim1| × |dim2| × ... × |dimN|
            
        Example:
            register_api("torch.nn.Conv2d", {
                "dtype": ["float16", "float32", "float64"],
                "device": ["cpu", "cuda"],
                "layout": ["strided"]
            })
            # Denominator = 3 × 2 × 1 = 6
        """
        if dimensions is None:
            # 使用简化的默认维度 (避免组合爆炸)
            dimensions = {
                "dtype": self.DEFAULT_DTYPES,
                "device": self.DEFAULT_DEVICES,
            }
        
        self.api_dimensions[api_name] = dimensions
        
        # 计算分母 (理论全集大小)
        # 公式: Denominator = ∏|dim_i|
        denominator = 1
        for dim_name, dim_values in dimensions.items():
            denominator *= len(dim_values)
        
        self.api_denominator[api_name] = denominator
        
        print(f"[DispatcherSpace] Registered API: {api_name}")
        print(f"  Dimensions: {list(dimensions.keys())}")
        print(f"  Theoretical Space (Denominator): {denominator}")
    
    def _extract_state_from_args(self, api: TorchAPI) -> Dict[str, str]:
        """
        从 TorchAPI 对象中提取当前的状态 (dtype, device, layout, etc.)
        
        核心逻辑:
        1. 遍历所有参数
        2. 对于 TORCH_TENSOR 类型，提取 dtype, shape 等信息
        3. 对于 TORCH_DTYPE 类型，直接提取 dtype
        4. 对于 TORCH_OBJECT 类型，检查是否是 memory_format
        
        Returns:
            状态字典，如 {"dtype": "float32", "device": "cpu", ...}
        """
        state = {
            "dtype": "unknown",
            "device": "cpu",  # 默认 CPU
            "layout": "strided",  # 默认 strided
        }
        
        for param_name, arg in api.args.items():
            if arg is None:
                continue
            
            # 处理 Tensor 参数
            if hasattr(arg, 'type') and arg.type == ArgType.TORCH_TENSOR:
                if hasattr(arg, 'dtype') and arg.dtype is not None:
                    # 提取 dtype 名称，如 "torch.float32" -> "float32"
                    dtype_str = str(arg.dtype)
                    if 'torch.' in dtype_str:
                        dtype_str = dtype_str.split('.')[-1]
                    state["dtype"] = dtype_str
                
                # 检查 shape 来推断可能的 layout
                if hasattr(arg, 'shape') and arg.shape:
                    # 简化处理：目前只考虑 strided
                    pass
            
            # 处理显式的 dtype 参数
            elif hasattr(arg, 'type') and arg.type == ArgType.TORCH_DTYPE:
                if hasattr(arg, 'value') and arg.value is not None:
                    dtype_str = str(arg.value)
                    if 'torch.' in dtype_str:
                        dtype_str = dtype_str.split('.')[-1]
                    state["dtype"] = dtype_str
            
            # 处理 memory_format 等对象
            elif hasattr(arg, 'type') and arg.type == ArgType.TORCH_OBJECT:
                if hasattr(arg, 'value'):
                    val_str = str(arg.value)
                    if 'memory_format' in val_str.lower():
                        # 提取 memory_format 类型
                        if 'channels_last' in val_str:
                            state["memory_format"] = "channels_last"
                        elif 'contiguous' in val_str:
                            state["memory_format"] = "contiguous_format"
        
        return state
    
    def record_hit(self, api_name: str, api: Optional[TorchAPI] = None, 
                   state_dict: Optional[Dict[str, str]] = None,
                   iteration: Optional[int] = None) -> bool:
        """
        记录一次成功的参数组合
        
        Args:
            api_name: API 名称
            api: TorchAPI 对象，如果提供则自动提取状态
            state_dict: 直接提供的状态字典，如 {"dtype": "float32", "device": "cpu"}
            iteration: 当前迭代次数，用于记录历史
        
        Returns:
            bool: 是否是一个新的组合 (True = 新发现，False = 已存在)
        
        Note:
            如果同时提供 api 和 state_dict，优先使用 state_dict
        """
        self.total_record_calls += 1
        
        # 确保 API 已注册
        if api_name not in self.api_dimensions:
            self.register_api(api_name)
        
        # 提取状态
        if state_dict is None and api is not None:
            state_dict = self._extract_state_from_args(api)
        elif state_dict is None:
            state_dict = {"dtype": "unknown", "device": "cpu"}
        
        # 过滤只保留已定义的维度
        dimensions = self.api_dimensions[api_name]
        filtered_state = {}
        for dim_name in dimensions.keys():
            if dim_name in state_dict:
                value = state_dict[dim_name]
                # 验证值是否在定义的范围内
                if value in dimensions[dim_name]:
                    filtered_state[dim_name] = value
                else:
                    # 值不在范围内，使用 "other" 标记
                    filtered_state[dim_name] = "other"
            else:
                filtered_state[dim_name] = "unknown"
        
        # 转换为 frozenset 便于哈希和去重
        state_key = frozenset(filtered_state.items())
        
        # 检查是否是新组合
        is_new = state_key not in self.api_hits[api_name]
        
        if is_new:
            self.api_hits[api_name].add(state_key)
            self.total_unique_hits += 1
        
        # 记录历史
        if iteration is not None:
            current_coverage = self.get_overall_coverage()
            self.coverage_history.append((iteration, current_coverage))
        
        return is_new
    
    def get_coverage(self, api_name: str) -> Tuple[int, int, float]:
        """
        获取指定 API 的覆盖率
        
        Returns:
            (numerator, denominator, percentage)
            numerator: 已覆盖的组合数
            denominator: 理论全集大小
            percentage: 覆盖率百分比
        """
        if api_name not in self.api_dimensions:
            return (0, 0, 0.0)
        
        numerator = len(self.api_hits[api_name])
        denominator = self.api_denominator[api_name]
        percentage = (numerator / denominator * 100) if denominator > 0 else 0.0
        
        return (numerator, denominator, percentage)
    
    def get_overall_coverage(self) -> float:
        """
        获取所有已注册 API 的平均覆盖率
        
        计算公式:
            Overall = (∑ Numerator_i) / (∑ Denominator_i) × 100%
        """
        total_numerator = 0
        total_denominator = 0
        
        for api_name in self.api_dimensions.keys():
            total_numerator += len(self.api_hits[api_name])
            total_denominator += self.api_denominator[api_name]
        
        if total_denominator == 0:
            return 0.0
        
        return (total_numerator / total_denominator) * 100
    
    def get_uncovered_combinations(self, api_name: str, max_show: int = 10) -> List[Dict[str, str]]:
        """
        获取未覆盖的参数组合
        
        Args:
            api_name: API 名称
            max_show: 最多返回多少个组合
        
        Returns:
            未覆盖的组合列表
        """
        if api_name not in self.api_dimensions:
            return []
        
        dimensions = self.api_dimensions[api_name]
        covered = self.api_hits[api_name]
        
        # 生成所有可能的组合
        dim_names = list(dimensions.keys())
        dim_values = [dimensions[name] for name in dim_names]
        
        uncovered = []
        for combo in itertools.product(*dim_values):
            state_dict = dict(zip(dim_names, combo))
            state_key = frozenset(state_dict.items())
            
            if state_key not in covered:
                uncovered.append(state_dict)
                if len(uncovered) >= max_show:
                    break
        
        return uncovered
    
    def print_summary(self):
        """
        打印详细的覆盖率报告
        """
        print(f"\n{'='*70}")
        print(f"📊 DISPATCHER STATE COVERAGE REPORT: {self.name}")
        print(f"{'='*70}")
        
        print(f"\n📈 Overall Statistics:")
        print(f"  Total record_hit calls: {self.total_record_calls}")
        print(f"  Unique combinations discovered: {self.total_unique_hits}")
        print(f"  Overall Coverage: {self.get_overall_coverage():.2f}%")
        
        print(f"\n📋 Per-API Coverage:")
        print(f"  {'API Name':<40} {'Covered':>8} {'Total':>8} {'Coverage':>10}")
        print(f"  {'-'*66}")
        
        for api_name in sorted(self.api_dimensions.keys()):
            num, denom, pct = self.get_coverage(api_name)
            print(f"  {api_name:<40} {num:>8} {denom:>8} {pct:>9.2f}%")
        
        # 显示未覆盖的组合 (仅限第一个 API)
        if self.api_dimensions:
            first_api = list(self.api_dimensions.keys())[0]
            uncovered = self.get_uncovered_combinations(first_api, max_show=5)
            
            if uncovered:
                print(f"\n❌ Sample Uncovered Combinations for {first_api}:")
                for combo in uncovered:
                    combo_str = ", ".join([f"{k}={v}" for k, v in combo.items()])
                    print(f"    - {combo_str}")
        
        print(f"\n{'='*70}\n")
    
    def to_dict(self) -> Dict:
        """导出为字典格式，便于 JSON 序列化"""
        result = {
            "name": self.name,
            "total_record_calls": self.total_record_calls,
            "total_unique_hits": self.total_unique_hits,
            "overall_coverage": self.get_overall_coverage(),
            "api_coverage": {}
        }
        
        for api_name in self.api_dimensions.keys():
            num, denom, pct = self.get_coverage(api_name)
            result["api_coverage"][api_name] = {
                "numerator": num,
                "denominator": denom,
                "percentage": pct
            }
        
        return result


# =============================================================================
# CSVLogger (流式日志写入器)
# =============================================================================

class CSVLogger:
    """
    流式 CSV 日志写入器
    ===================
    
    优势:
    - 流式写入，避免内存溢出
    - 支持断点续写
    - 自动 flush 确保数据安全
    
    列定义:
    - iteration: 迭代次数
    - timestamp: Unix 时间戳
    - phase: warm-up / evolution
    - source: random / corpus / exploration
    - strategy: 当前使用的策略
    - valid: 是否执行成功
    - new_kernels: 新发现的 kernel 数量
    - total_kernels: 累计 kernel 数量
    - corpus_size: Corpus 大小
    - dispatcher_coverage: Dispatcher 状态覆盖率
    - bug_count: 累计 Bug 数量
    """
    
    COLUMNS = [
        "iteration", "timestamp", "phase", "source", "strategy",
        "valid", "new_kernels", "total_kernels", "corpus_size",
        "dispatcher_coverage", "bug_count", "features"
    ]
    
    def __init__(self, output_file: str, strategy: str = "hkg"):
        """
        初始化 CSVLogger
        
        Args:
            output_file: 输出文件路径
            strategy: 策略名称
        """
        self.output_file = output_file
        self.strategy = strategy
        self.row_count = 0
        
        # 如果文件已存在，追加模式；否则创建并写入表头
        file_exists = os.path.exists(output_file)
        
        self.file_handle = open(output_file, 'a', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file_handle, fieldnames=self.COLUMNS)
        
        if not file_exists:
            self.writer.writeheader()
            self.file_handle.flush()
        
        print(f"[CSVLogger] Logging to: {output_file}")
    
    def log(self, 
            iteration: int,
            phase: str,
            source: str,
            valid: bool,
            new_kernels: int = 0,
            total_kernels: int = 0,
            corpus_size: int = 0,
            dispatcher_coverage: float = 0.0,
            bug_count: int = 0,
            features: str = ""):
        """
        记录一行日志
        """
        row = {
            "iteration": iteration,
            "timestamp": time.time(),
            "phase": phase,
            "source": source,
            "strategy": self.strategy,
            "valid": valid,
            "new_kernels": new_kernels,
            "total_kernels": total_kernels,
            "corpus_size": corpus_size,
            "dispatcher_coverage": round(dispatcher_coverage, 4),
            "bug_count": bug_count,
            "features": features
        }
        
        self.writer.writerow(row)
        self.row_count += 1
        
        # 每 100 行 flush 一次
        if self.row_count % 100 == 0:
            self.file_handle.flush()
    
    def close(self):
        """关闭文件句柄"""
        if self.file_handle:
            self.file_handle.flush()
            self.file_handle.close()
    
    def __del__(self):
        self.close()


# =============================================================================
# 以下是从原始 benchmark_full_oracle.py 复制的辅助类
# (保持原有功能不变)
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
    
    def check_and_cleanup(self) -> Tuple[bool, str]:
        total, used, free = self.get_disk_usage()
        if free < self.min_free_gb:
            self.warnings += 1
            if self.auto_cleanup:
                # 清理临时文件
                count = 0
                for temp_file in self.output_dir.rglob("temp.py"):
                    try:
                        temp_file.unlink()
                        count += 1
                    except:
                        pass
                if count > 0:
                    self.cleanups += 1
                total, used, free = self.get_disk_usage()
            return free < self.min_free_gb, f"Disk: {free:.2f} GB free"
        return False, ""
    
    def get_status(self) -> str:
        total, used, free = self.get_disk_usage()
        return f"{free:.2f} GB free ({used/total*100:.1f}% used)"


class OutlierFilter:
    """异常参数过滤 - 防止 OOM"""
    def __init__(self, max_elements: int = int(1e8)):
        self.max_elements = max_elements
        self.total_checks = 0
        self.filtered_count = 0
    
    def check_api(self, api) -> Tuple[bool, Optional[str]]:
        self.total_checks += 1
        for param_name, arg in api.args.items():
            if arg is None:
                continue
            if hasattr(arg, 'type') and arg.type == ArgType.TORCH_TENSOR:
                if hasattr(arg, 'shape') and arg.shape:
                    num_elements = 1
                    for dim in arg.shape:
                        num_elements *= dim
                    if num_elements > self.max_elements:
                        self.filtered_count += 1
                        return True, f"Too many elements: {num_elements}"
        return False, None
    
    def get_status(self) -> str:
        rate = (self.filtered_count / self.total_checks * 100) if self.total_checks > 0 else 0
        return f"{self.filtered_count}/{self.total_checks} filtered ({rate:.1f}%)"


class EvolutionaryCorpus:
    """进化种子池"""
    
    def __init__(self, max_size: int = 100):
        self.corpus: List[TorchAPI] = []
        self.max_size = max_size
        # 记录每个种子发现的 kernel 数量，用于优先选择
        self.seed_scores: List[int] = []
    
    def add_seed(self, api: TorchAPI, discovered_kernels: Set[str]):
        if len(discovered_kernels) == 0:
            return
        
        seed_copy = copy.deepcopy(api)
        self.corpus.append(seed_copy)
        self.seed_scores.append(len(discovered_kernels))
        
        if len(self.corpus) > self.max_size:
            self.corpus.pop(0)
            self.seed_scores.pop(0)
    
    def select_parent(self) -> Optional[TorchAPI]:
        """加权随机选择，优先选择发现更多 kernel 的种子"""
        if not self.corpus:
            return None
        
        # 使用分数作为权重
        total_score = sum(self.seed_scores) or 1
        probs = [s / total_score for s in self.seed_scores]
        
        idx = np.random.choice(len(self.corpus), p=probs)
        return self.corpus[idx]
    
    def size(self) -> int:
        return len(self.corpus)


class EnhancedCoverageTracker:
    """覆盖率追踪器"""
    
    def __init__(self, name: str):
        self.name = name
        self.all_kernels: Set[str] = set()
        self.kernel_provenance: Dict[str, int] = {}
        self.history: List[Tuple[int, int]] = []
        self.new_kernel_iterations: List[int] = []
    
    def update(self, new_kernels: Set[str], iteration: int) -> int:
        """更新覆盖率，返回新发现的 kernel 数量"""
        if not isinstance(new_kernels, set):
            new_kernels = set(new_kernels) if new_kernels else set()
        
        fresh = new_kernels - self.all_kernels
        
        if fresh:
            for kernel in fresh:
                self.kernel_provenance[kernel] = iteration
            self.all_kernels.update(fresh)
            self.new_kernel_iterations.append(iteration)
        
        self.history.append((iteration, len(self.all_kernels)))
        return len(fresh)
    
    def get_total(self) -> int:
        return len(self.all_kernels)


class BugTracker:
    """Bug 追踪器"""
    def __init__(self, name: str, output_dir: str):
        self.name = name
        self.output_dir = output_dir
        self.bugs = {"crash": [], "cuda": [], "precision": []}
        self.bug_files = {"crash": set(), "cuda": set(), "precision": set()}
        
    def scan_bugs(self):
        oracle_map = {"crash": "crash-oracle", "cuda": "cuda-oracle", "precision": "precision-oracle"}
        for bug_type, oracle_name in oracle_map.items():
            bug_dir = join(self.output_dir, oracle_name, "potential-bug")
            if not os.path.exists(bug_dir):
                continue
            for root, _, files in os.walk(bug_dir):
                for f in files:
                    if not f.endswith('.py'): continue
                    file_path = join(root, f)
                    if file_path not in self.bug_files[bug_type]:
                        self.bug_files[bug_type].add(file_path)
                        self.bugs[bug_type].append((len(self.bugs[bug_type]), "unknown", file_path))

    def get_total_bugs(self) -> int:
        return sum(len(bugs) for bugs in self.bugs.values())
    
    def get_bugs_by_type(self, bug_type: str) -> int:
        return len(self.bugs.get(bug_type, []))


# =============================================================================
# Mutation Patchers (保持与原始实现兼容)
# =============================================================================

_ORIGINAL_DO_SELECT_FROM_DB = None
_POISON_ORIGINAL_FLOAT = None
_POISON_ORIGINAL_INT = None

class ProbabilityPatcher:
    """将数据库采样概率从 20% 提升到 50%"""
    
    @staticmethod
    def patch_high_db_probability():
        global _ORIGINAL_DO_SELECT_FROM_DB
        try:
            import utils.probability as prob_module
            _ORIGINAL_DO_SELECT_FROM_DB = prob_module.do_select_from_db
            
            def high_db_select() -> bool:
                from numpy.random import rand
                return rand() < 0.5
            
            prob_module.do_select_from_db = high_db_select
            print("[Patch] ✅ Database sampling: 20% → 50%")
        except ImportError:
            print("[Patch] ⚠️ utils.probability not found, skipping")
    
    @staticmethod
    def restore():
        global _ORIGINAL_DO_SELECT_FROM_DB
        if _ORIGINAL_DO_SELECT_FROM_DB:
            try:
                import utils.probability as prob_module
                prob_module.do_select_from_db = _ORIGINAL_DO_SELECT_FROM_DB
                print("[Patch] 🔄 Database sampling restored")
            except ImportError:
                pass


class PoisonPatcher:
    """
    独立的投毒补丁 - 对 Random 和 Guided 都生效
    """
    
    @staticmethod
    def patch():
        global _POISON_ORIGINAL_FLOAT, _POISON_ORIGINAL_INT
        
        _POISON_ORIGINAL_FLOAT = Argument.mutate_float_value
        _POISON_ORIGINAL_INT = Argument.mutate_int_value
        
        def poison_float_mutation(self, value) -> float:
            from numpy.random import rand, choice
            
            roll = rand()
            
            if roll < 0.05:
                return choice([float('inf'), float('-inf')])
            elif roll < 0.10:
                return float('nan')
            elif roll < 0.20:
                return choice([1e20, -1e20, 1e-10, -1e-10])
            elif roll < 0.50:
                return choice(Argument._float_values)
            else:
                return value + (rand() - 0.5) * 8.0
        
        def poison_int_mutation(self, value, _min=None, _max=None) -> int:
            from numpy.random import rand, choice, randint
            
            roll = rand()
            
            if roll < 0.10:
                new_value = choice([0, -1, 1])
            elif roll < 0.20:
                new_value = choice([-999, 999, -2147483648, 2147483647])
            elif roll < 0.30:
                new_value = choice([-2, -3, 256, 512, 7, 11, 0])
            elif roll < 0.60:
                new_value = choice(Argument._int_values)
            else:
                new_value = value + randint(-8, 9)
            
            if _min is not None and new_value < _min and new_value not in [-1, 0]:
                new_value = max(_min, new_value)
            if _max is not None and new_value > _max:
                new_value = min(_max, new_value)
            
            return int(new_value)
        
        Argument.mutate_float_value = poison_float_mutation 
        Argument.mutate_int_value = poison_int_mutation
        print("[Patch] 🧪 Poison Injection enabled")
    
    @staticmethod
    def restore():
        global _POISON_ORIGINAL_FLOAT, _POISON_ORIGINAL_INT
        if _POISON_ORIGINAL_FLOAT:
            Argument.mutate_float_value = _POISON_ORIGINAL_FLOAT
        if _POISON_ORIGINAL_INT:
            Argument.mutate_int_value = _POISON_ORIGINAL_INT
        print("[Patch] 🔄 Poison Injection restored")


# =============================================================================
# 🔥 HKGFuzzEngine - 混合热启动 Fuzzer
# =============================================================================

class HKGFuzzEngine:
    """
    Hybrid Kernel-Guided Fuzz Engine
    =================================
    
    核心论点:
    ---------
    1. Random Fuzzing (FreeFuzz): 吞吐量大，快速覆盖浅层状态，但容易饱和
    2. Kernel-Guided Fuzzing: 穿透力强，覆盖深层状态，但冷启动慢
    3. 最优策略: "Warm-up with Random" → "Evolve with Kernel-Guided"
    
    执行流程:
    ---------
    Phase 1 (Warm-up):
        - 前 warmup_ratio (默认 10%) 的迭代
        - 强制使用 Random 策略
        - 目标: 快速填满 Corpus，快速点亮 DispatcherSpace 的浅层格子
    
    Phase 2 (Evolution):
        - 切换到 Kernel-Guided 模式
        - ε-greedy: 90% 利用 + 10% 探索
        - 结构化投毒: NaN, Inf, 边界值
        - 动态调整: 停滞时扩大搜索范围
    
    度量:
    -----
    - Kernel Coverage: 触发的 CUDA kernel 数量
    - Dispatcher State Coverage: 分发器状态覆盖率 (创新点)
    - Bug Count: 发现的 Bug 数量
    """
    
    def __init__(self,
                 api_name: str,
                 output_dir: str,
                 warmup_ratio: float = 0.1,
                 use_all_oracles: bool = True,
                 enable_dispatcher_space: bool = True,
                 enable_csv_logging: bool = True,
                 diff_bound: float = 1e-5):
        """
        初始化 HKGFuzzEngine
        
        Args:
            api_name: 要测试的 API 名称，如 "torch.nn.LSTM"
            output_dir: 输出目录
            warmup_ratio: 热启动阶段的迭代比例，默认 10%
            use_all_oracles: 是否使用所有 Oracle (CRASH + CUDA + PRECISION)
            enable_dispatcher_space: 是否启用 Dispatcher 状态覆盖率计算
            enable_csv_logging: 是否启用 CSV 日志
            diff_bound: 精度容差
        """
        self.api_name = api_name
        self.output_dir = output_dir
        self.warmup_ratio = warmup_ratio
        self.use_all_oracles = use_all_oracles
        self.enable_dispatcher_space = enable_dispatcher_space
        self.diff_bound = diff_bound
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 初始化 Library
        self.library = TorchLibrary(output_dir, diff_bound=diff_bound)
        
        # Oracle 列表
        if use_all_oracles:
            self.oracles = [OracleType.CRASH, OracleType.CUDA, OracleType.PRECISION]
        else:
            self.oracles = [OracleType.CRASH]
        
        # Coverage Tracker
        self.coverage = EnhancedCoverageTracker("HKG")
        
        # Bug Tracker
        self.bug_tracker = BugTracker("HKG", output_dir)
        
        # Evolutionary Corpus
        self.corpus = EvolutionaryCorpus(max_size=100)
        
        # Dispatcher Space (创新点)
        self.dispatcher_space = None
        if enable_dispatcher_space:
            self.dispatcher_space = DispatcherSpace(name=api_name)
            self.dispatcher_space.register_api(api_name)
        
        # CSV Logger
        self.csv_logger = None
        if enable_csv_logging:
            api_clean = api_name.replace('.', '_').replace('::', '_')
            log_file = join(output_dir, f"{api_clean}_hkg_trace.csv")
            self.csv_logger = CSVLogger(log_file, strategy="hkg")
        
        # Safety Guards
        self.speedometer = Speedometer(window_size=100, slow_threshold=0.5)
        self.disk_guard = DiskGuard(output_dir, min_free_gb=1.0, auto_cleanup=True)
        self.outlier_filter = OutlierFilter(max_elements=int(1e8))
        
        # 状态
        self.current_phase = "init"
        self.warmup_end_iteration = 0
        
        # ε-greedy 参数
        self.epsilon = 0.1  # 10% 探索
        
        print(f"\n{'='*70}")
        print(f"🚀 HKGFuzzEngine Initialized")
        print(f"{'='*70}")
        print(f"  API: {api_name}")
        print(f"  Warm-up Ratio: {warmup_ratio*100:.0f}%")
        print(f"  Oracles: {[str(o) for o in self.oracles]}")
        print(f"  Dispatcher Space: {'Enabled' if enable_dispatcher_space else 'Disabled'}")
        print(f"  CSV Logging: {'Enabled' if enable_csv_logging else 'Disabled'}")
        print(f"{'='*70}\n")
    
    def _extract_features(self, api: TorchAPI) -> str:
        """提取 API 调用的参数指纹"""
        features = []
        for param_name, arg in api.args.items():
            if arg is None:
                continue
            if hasattr(arg, 'type'):
                if arg.type == ArgType.TORCH_TENSOR:
                    shape_str = str(arg.shape) if hasattr(arg, 'shape') else 'unknown'
                    dtype_str = str(arg.dtype).split(".")[-1] if hasattr(arg, 'dtype') else 'unknown'
                    features.append(f"{param_name}:tensor:{dtype_str}:{shape_str}")
                elif arg.type == ArgType.INT:
                    features.append(f"{param_name}:int:{arg.value}")
                elif arg.type == ArgType.FLOAT:
                    features.append(f"{param_name}:float:{arg.value:.2f}")
                elif arg.type == ArgType.BOOL:
                    features.append(f"{param_name}:bool:{arg.value}")
        features.sort()
        return "|".join(features)[:200]  # 限制长度
    
    def run(self, max_iterations: int = 10000, checkpoint_interval: int = 100):
        """
        运行 HKG Fuzzing
        
        Args:
            max_iterations: 最大迭代次数
            checkpoint_interval: 检查点间隔
        """
        print(f"\n{'='*70}")
        print(f"🔬 Starting HKG Fuzzing: {self.api_name}")
        print(f"{'='*70}")
        print(f"  Max Iterations: {max_iterations}")
        print(f"  Phase 1 (Warm-up): 0 → {int(max_iterations * self.warmup_ratio)}")
        print(f"  Phase 2 (Evolution): {int(max_iterations * self.warmup_ratio)} → {max_iterations}")
        print(f"{'='*70}\n")
        
        # 计算热启动结束点
        self.warmup_end_iteration = int(max_iterations * self.warmup_ratio)
        
        # 启动速度计
        self.speedometer.start()
        start_time = time.time()
        
        # 主循环
        for i in range(max_iterations):
            self.speedometer.tick()
            
            # =================================================================
            # 阶段判断
            # =================================================================
            if i < self.warmup_end_iteration:
                self.current_phase = "warmup"
                source = self._warmup_iteration(i)
            else:
                self.current_phase = "evolution"
                source = self._evolution_iteration(i)
            
            # =================================================================
            # 生成测试用例
            # =================================================================
            api = self._generate_test_case(source)
            
            # Outlier 过滤
            should_filter, _ = self.outlier_filter.check_api(api)
            if should_filter:
                self._log_iteration(i, source, api, valid=False)
                continue
            
            # =================================================================
            # 执行测试
            # =================================================================
            all_captured_kernels = set()
            execution_valid = False
            
            for oracle in self.oracles:
                try:
                    captured_kernels = self.library.test_with_oracle(api, oracle)
                    all_captured_kernels.update(captured_kernels)
                    execution_valid = True
                except Exception as e:
                    pass
            
            # =================================================================
            # 更新覆盖率
            # =================================================================
            new_count = self.coverage.update(all_captured_kernels, i)
            
            # 更新 Dispatcher Space
            if self.dispatcher_space and execution_valid:
                self.dispatcher_space.record_hit(self.api_name, api=api, iteration=i)
            
            # 更新 Corpus
            if new_count > 0:
                self.corpus.add_seed(api, all_captured_kernels)
            
            # 记录日志
            self._log_iteration(i, source, api, execution_valid, new_count)
            
            # =================================================================
            # 定期检查
            # =================================================================
            if (i + 1) % checkpoint_interval == 0:
                self._checkpoint(i, max_iterations, start_time)
        
        # =================================================================
        # 完成
        # =================================================================
        self._finalize(start_time)
    
    def _warmup_iteration(self, iteration: int) -> str:
        """
        Phase 1: Warm-up 阶段
        
        策略:
        - 100% Random: 快速生成多样化的种子
        - 目标: 填充 Corpus，点亮浅层状态格子
        """
        return "random"
    
    def _evolution_iteration(self, iteration: int) -> str:
        """
        Phase 2: Evolution 阶段
        
        策略:
        - ε-greedy: 90% 利用 Corpus，10% 探索
        """
        if random.random() < self.epsilon:
            return "exploration"
        elif self.corpus.size() > 0 and random.random() < 0.7:
            return "corpus"
        else:
            return "random"
    
    def _generate_test_case(self, source: str) -> TorchAPI:
        """
        生成测试用例
        """
        if source == "corpus" and self.corpus.size() > 0:
            parent_api = self.corpus.select_parent()
            api = copy.deepcopy(parent_api)
        else:
            api = TorchAPI(self.api_name)
        
        # 变异
        api.mutate()
        return api
    
    def _log_iteration(self, iteration: int, source: str, api: TorchAPI, 
                       valid: bool, new_kernels: int = 0):
        """记录日志"""
        if self.csv_logger:
            features = self._extract_features(api)
            dispatcher_cov = self.dispatcher_space.get_overall_coverage() if self.dispatcher_space else 0.0
            
            self.csv_logger.log(
                iteration=iteration,
                phase=self.current_phase,
                source=source,
                valid=valid,
                new_kernels=new_kernels,
                total_kernels=self.coverage.get_total(),
                corpus_size=self.corpus.size(),
                dispatcher_coverage=dispatcher_cov,
                bug_count=self.bug_tracker.get_total_bugs(),
                features=features
            )
    
    def _checkpoint(self, iteration: int, max_iterations: int, start_time: float):
        """定期检查点"""
        elapsed = time.time() - start_time
        
        # 扫描 Bug
        self.bug_tracker.scan_bugs()
        
        print(f"\n--- Checkpoint: {iteration+1}/{max_iterations} ({elapsed/60:.1f} min) ---")
        print(f"  Phase: {self.current_phase.upper()}")
        print(f"  Kernels: {self.coverage.get_total()}")
        print(f"  Corpus: {self.corpus.size()} seeds")
        print(f"  Bugs: {self.bug_tracker.get_total_bugs()}")
        
        if self.dispatcher_space:
            print(f"  Dispatcher Coverage: {self.dispatcher_space.get_overall_coverage():.2f}%")
        
        print(f"  Speed: {self.speedometer.get_status(iteration, max_iterations)}")
        print(f"  Disk: {self.disk_guard.get_status()}")
        
        # 磁盘检查
        is_critical, msg = self.disk_guard.check_and_cleanup()
        if is_critical:
            print(f"\n⚠️ {msg}")
    
    def _finalize(self, start_time: float):
        """完成并输出报告"""
        elapsed = time.time() - start_time
        
        # 最终 Bug 扫描
        self.bug_tracker.scan_bugs()
        
        print(f"\n{'='*70}")
        print(f"✅ HKG Fuzzing Completed: {self.api_name}")
        print(f"{'='*70}")
        print(f"  Total Time: {elapsed/60:.1f} minutes")
        print(f"  Total Kernels: {self.coverage.get_total()}")
        print(f"  Total Bugs: {self.bug_tracker.get_total_bugs()}")
        print(f"    - Crash: {self.bug_tracker.get_bugs_by_type('crash')}")
        print(f"    - CUDA: {self.bug_tracker.get_bugs_by_type('cuda')}")
        print(f"    - Precision: {self.bug_tracker.get_bugs_by_type('precision')}")
        print(f"  Corpus Size: {self.corpus.size()}")
        print(f"  Average Speed: {self.speedometer.get_average_speed():.2f} it/s")
        
        # Dispatcher Space 报告
        if self.dispatcher_space:
            self.dispatcher_space.print_summary()
        
        # 关闭日志
        if self.csv_logger:
            self.csv_logger.close()
            print(f"\n📝 CSV Log saved: {self.csv_logger.output_file}")
        
        # 保存结果
        self._save_results()
        
        print(f"{'='*70}\n")
    
    def _save_results(self):
        """保存结果到 JSON"""
        results = {
            "api": self.api_name,
            "strategy": "HKG (Hybrid Kernel-Guided)",
            "warmup_ratio": self.warmup_ratio,
            "total_kernels": self.coverage.get_total(),
            "bugs": {
                "total": self.bug_tracker.get_total_bugs(),
                "crash": self.bug_tracker.get_bugs_by_type("crash"),
                "cuda": self.bug_tracker.get_bugs_by_type("cuda"),
                "precision": self.bug_tracker.get_bugs_by_type("precision")
            },
            "corpus_size": self.corpus.size()
        }
        
        if self.dispatcher_space:
            results["dispatcher_space"] = self.dispatcher_space.to_dict()
        
        result_file = join(self.output_dir, f"{self.api_name.replace('.', '_')}_hkg_results.json")
        with open(result_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved: {result_file}")


# =============================================================================
# Visualization (与原始实现兼容)
# =============================================================================

def plot_hkg_results(coverage: EnhancedCoverageTracker,
                     dispatcher_space: Optional[DispatcherSpace],
                     bug_tracker: BugTracker,
                     api_name: str,
                     output_dir: str):
    """绘制 HKG 结果图"""
    
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Kernel 覆盖率曲线
    ax1 = fig.add_subplot(gs[0, 0])
    if coverage.history:
        iters, kernels = zip(*coverage.history)
        ax1.plot(iters, kernels, color="#e74c3c", linewidth=2)
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Cumulative Kernels")
    ax1.set_title("A) Kernel Coverage")
    ax1.grid(True, alpha=0.3)
    
    # Dispatcher 状态覆盖率
    ax2 = fig.add_subplot(gs[0, 1])
    if dispatcher_space and dispatcher_space.coverage_history:
        iters, cov = zip(*dispatcher_space.coverage_history)
        ax2.plot(iters, cov, color="#3498db", linewidth=2)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Coverage (%)")
    ax2.set_title("B) Dispatcher State Coverage")
    ax2.grid(True, alpha=0.3)
    
    # Bug 统计
    ax3 = fig.add_subplot(gs[1, 0])
    bug_types = ['Crash', 'CUDA', 'Precision']
    bug_counts = [
        bug_tracker.get_bugs_by_type('crash'),
        bug_tracker.get_bugs_by_type('cuda'),
        bug_tracker.get_bugs_by_type('precision')
    ]
    bars = ax3.bar(bug_types, bug_counts, color=['#e74c3c', '#f39c12', '#9b59b6'])
    ax3.set_ylabel("Count")
    ax3.set_title("C) Bugs by Type")
    for bar, count in zip(bars, bug_counts):
        if count > 0:
            ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{int(count)}', ha='center', va='bottom')
    
    # 统计表
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    stats_text = f"""
    HKG Fuzzing Statistics
    ━━━━━━━━━━━━━━━━━━━━━━━━━
    
    API: {api_name}
    
    Kernel Coverage:
      Total Kernels: {coverage.get_total()}
    
    Dispatcher Coverage:
      Overall: {dispatcher_space.get_overall_coverage() if dispatcher_space else 'N/A':.2f}%
    
    Bugs Found:
      Total: {bug_tracker.get_total_bugs()}
      Crash: {bug_tracker.get_bugs_by_type('crash')}
      CUDA: {bug_tracker.get_bugs_by_type('cuda')}
      Precision: {bug_tracker.get_bugs_by_type('precision')}
    """
    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace')
    ax4.set_title("D) Summary")
    
    fig.suptitle(f"HKG Fuzzing Results: {api_name}", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    plot_file = join(output_dir, f"{api_name.replace('.', '_')}_hkg_plot.png")
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n📊 Plot saved: {plot_file}")


# =============================================================================
# Main Experiment Runner
# =============================================================================

def run_hkg_experiment(
    api_name: str,
    max_iterations: int,
    output_dir: str,
    config_file: str = "demo_torch.conf",
    warmup_ratio: float = 0.1,
    diff_bound: float = 1e-5
):
    """
    运行 HKG 实验
    
    Args:
        api_name: API 名称
        max_iterations: 最大迭代次数
        output_dir: 输出目录
        config_file: 配置文件
        warmup_ratio: 热启动比例
        diff_bound: 精度容差
    """
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
        print("⚠️ Config file not found, using default settings")
    else:
        print(f"📁 Config: {os.path.abspath(config_path)}")
        config.read(config_path)
        
        TorchDatabase.database_config(
            config["mongodb"]["host"],
            int(config["mongodb"]["port"]),
            config["mongodb"]["torch_database"]
        )
    
    # 启用投毒
    PoisonPatcher.patch()
    ProbabilityPatcher.patch_high_db_probability()
    
    try:
        # 创建并运行 HKGFuzzEngine
        engine = HKGFuzzEngine(
            api_name=api_name,
            output_dir=output_dir,
            warmup_ratio=warmup_ratio,
            use_all_oracles=True,
            enable_dispatcher_space=True,
            enable_csv_logging=True,
            diff_bound=diff_bound
        )
        
        engine.run(
            max_iterations=max_iterations,
            checkpoint_interval=max(100, max_iterations // 20)
        )
        
        # 绘图
        plot_hkg_results(
            engine.coverage,
            engine.dispatcher_space,
            engine.bug_tracker,
            api_name,
            output_dir
        )
        
    finally:
        ProbabilityPatcher.restore()
        PoisonPatcher.restore()


# =============================================================================
# Main
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="HKG (Hybrid Kernel-Guided) Fuzzing Benchmark"
    )
    parser.add_argument("--api", type=str, default="torch.nn.LSTM",
                        help="API to test")
    parser.add_argument("--max-iterations", type=int, default=10000,
                        help="Maximum iterations")
    parser.add_argument("--output", type=str, default="hkg_output")
    parser.add_argument("--conf", type=str, default="demo_torch.conf")
    parser.add_argument("--warmup-ratio", type=float, default=0.1,
                        help="Warm-up phase ratio (default: 0.1 = 10%)")
    parser.add_argument("--diff-bound", type=float, default=1e-5,
                        help="Precision tolerance")
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔬 HKG (HYBRID KERNEL-GUIDED) FUZZING")
    print("="*70)
    print(f"API: {args.api}")
    print(f"Max Iterations: {args.max_iterations:,}")
    print(f"Warm-up Ratio: {args.warmup_ratio*100:.0f}%")
    print(f"  Phase 1 (Warm-up): 0 → {int(args.max_iterations * args.warmup_ratio)}")
    print(f"  Phase 2 (Evolution): {int(args.max_iterations * args.warmup_ratio)} → {args.max_iterations}")
    print(f"Oracles: CRASH + CUDA + PRECISION")
    print("="*70)
    
    run_hkg_experiment(
        api_name=args.api,
        max_iterations=args.max_iterations,
        output_dir=args.output,
        config_file=args.conf,
        warmup_ratio=args.warmup_ratio,
        diff_bound=args.diff_bound
    )


if __name__ == "__main__":
    main()