# -*- coding: utf-8 -*-
"""
Kernel-Guided Fuzzing Benchmark - Full Oracle Edition with Hybrid Strategy
==========================================================================

æ ¸å¿ƒå¢žå¼º:
1. **æ··åˆç­–ç•¥**: Îµ-greedy (90% å¾®åˆ› + 10% æŽ¢ç´¢)
2. **åŠ¨æ€å˜å¼‚**: åœæ»žæ—¶è‡ªåŠ¨æ‰©å¤§å˜å¼‚èŒƒå›´
3. **å–æ¶ˆé¥±å’Œåœæ­¢**: æ”¹ä¸º"æ‰©å¤§æœç´¢"è€Œéž"ç»ˆæ­¢"
4. **å…¨ Oracle æ”¯æŒ**: CRASH + CUDA + PRECISION
5. **æ™ºèƒ½å½’ç±»**: åŸºäºŽé”™è¯¯æŒ‡çº¹çš„ Bug åŽ»é‡ä¸Žåˆ†ç±» (New!)

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
import gc
from os.path import join
from pathlib import Path
from typing import Set, List, Dict, Tuple, Optional
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import numpy as np
import time
import torch

# FreeFuzz imports
from classes.database import TorchDatabase
from classes.torch_api import TorchAPI, TorchArgument
from classes.torch_library import TorchLibrary
from classes.argument import Argument, ArgType
from constants.enum import OracleType


# =============================================================================
# Safety Guards (ä¿æŠ¤æœºåˆ¶)
# =============================================================================

class Speedometer:
    """é€Ÿåº¦ç›‘æŽ§ - åŠæ—¶å‘çŽ°æ€§èƒ½é—®é¢˜"""
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
            warning = (f"âš ï¸  SLOW SPEED: {current_speed:.2f} it/s (threshold: {self.slow_threshold})")
            if current_speed < 0.1:
                warning += "\n   â†’ Check if Precision Oracle is too slow"
            elif current_speed < 0.5:
                warning += "\n   â†’ Consider reducing complexity or disabling oracles"
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
    """ç£ç›˜ç©ºé—´ç›‘æŽ§ - é˜²æ­¢çˆ†æ»¡å´©æºƒ"""
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
            warning = f"âš ï¸  DISK SPACE: Only {free:.2f} GB free (threshold: {self.min_free_gb} GB)"
            if self.auto_cleanup:
                warning += "\n   â†’ Attempting auto-cleanup..."
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
            message = f"{warning}\n   Cleaned {cleaned} files â†’ {free:.2f} GB free"
            if free < self.min_free_gb:
                message += "\n   âŒ CRITICAL: Still low after cleanup!"
                return True, message
            message += "\n   âœ… Cleanup successful"
            return False, message
        return True, warning
    
    def get_status(self) -> str:
        total, used, free = self.get_disk_usage()
        return f"{free:.2f} GB free ({used/total*100:.1f}% used)"


class OutlierFilter:
    """å¼‚å¸¸å‚æ•°è¿‡æ»¤ - é˜²æ­¢ OOM"""
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
# Checkpoint System (æ–­ç‚¹ç»­ä¼ )
# =============================================================================

class CheckpointManager:
    """æ£€æŸ¥ç‚¹ç®¡ç†å™¨ - æ”¯æŒæ–­ç‚¹ç»­ä¼ """
    
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
            print(f"[Checkpoint] âŒ Save failed: {e}")
            return False
    
    def load(self) -> Optional[Dict]:
        if not self.checkpoint_file.exists():
            return None
        
        try:
            with open(self.checkpoint_file, 'rb') as f:
                data = pickle.load(f)
            
            print(f"[Checkpoint] âœ… Loaded from iteration {data['iteration']}")
            print(f"  Kernels: {len(data['coverage_kernels'])}")
            if data.get('corpus_seeds'):
                print(f"  Corpus: {len(data['corpus_seeds'])} seeds")
            
            return data
            
        except Exception as e:
            print(f"[Checkpoint] âŒ Load failed: {e}")
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
# Feature Extractor (å‚æ•°æŒ‡çº¹æå–)
# =============================================================================

def extract_features(api: TorchAPI) -> str:
    """
    æå– API è°ƒç”¨çš„å‚æ•°æŒ‡çº¹ï¼Œç”¨äºŽåŽç»­çš„ç‰¹å¾å¤šæ ·æ€§åˆ†æž
    
    è¿”å›žæ ¼å¼: "param1:type1:value1|param2:type2:value2|..."
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
# Experiment Logger (åŽŸå§‹æ•°æ®è®°å½•å™¨)
# =============================================================================

class ExperimentLogger:
    """è½»é‡çº§å®žéªŒæ•°æ®è®°å½•å™¨"""
    
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

# ä¿å­˜åŽŸå§‹æ–¹æ³•
_ORIGINAL_DO_SELECT_FROM_DB = None
_ORIGINAL_MUTATE_INT_VALUE = None
_ORIGINAL_MUTATE_FLOAT_VALUE = None


# =============================================================================
# Bug Tracker (Bug è¿½è¸ªå™¨) - ðŸ”¥ å‡çº§ç‰ˆï¼šæŒ‡çº¹è¯†åˆ«
# =============================================================================

class BugAnalyzer:
    """æ›´ç²¾ç»†çš„ Bug åˆ†æžå™¨ï¼Œæ”¯æŒé”™è¯¯æŒ‡çº¹æå–"""
    
    # ç”¨äºŽæ¸…æ´—é”™è¯¯ä¿¡æ¯ä¸­çš„æ•°å­—ã€åœ°å€ã€Shape
    REGEX_PATTERNS = [
        (r'0x[0-9a-fA-F]+', 'ADDR'),           # æ›¿æ¢å†…å­˜åœ°å€
        (r'\d+\.\d+', 'FLOAT'),                # æ›¿æ¢æµ®ç‚¹æ•°
        (r'\d+', 'INT'),                       # æ›¿æ¢æ•´æ•°
        (r'\[.*?\]', '[SHAPE]'),               # æ›¿æ¢ Tensor Shape æè¿°
        (r'\s+', ' '),                         # åˆå¹¶ç©ºæ ¼
    ]

    @staticmethod
    def get_signature(content: str) -> str:
        """基于代码特征生成指纹（bug文件只保存代码，不保存错误信息）"""
        if not content:
            return "unknown_empty"
        
        features = []
        
        # 1. 提取 dtype（最重要的区分特征）
        dtype_matches = re.findall(r'dtype\s*=\s*(torch\.[a-z0-9]+)', content)
        if dtype_matches:
            unique_dtypes = sorted(set(dtype_matches))
            features.append(f"dtype={','.join(unique_dtypes)}")
        
        # 2. 提取 tensor 维度数（归一化 shape）
        shape_matches = re.findall(r'torch\.rand(?:int)?\s*\(\s*[\[\(]([^\]\)]+)[\]\)]', content)
        if shape_matches:
            for shape in shape_matches[:2]:
                ndim = shape.count(',') + 1
                features.append(f"ndim={ndim}")
                break
        
        # 3. 提取特殊值特征（投毒触发的关键）
        if re.search(r'\bnan\b', content, re.IGNORECASE):
            features.append("NaN")
        if re.search(r'\binf\b', content, re.IGNORECASE):
            features.append("Inf")
        
        # 4. 生成指纹
        if not features:
            return f"hash={hashlib.md5(content.encode()).hexdigest()[:12]}"
        
        return "|".join(sorted(features))

    @staticmethod
    def classify_bug(error_msg: str) -> str:
        """åˆ†ç±»é€»è¾‘ï¼ˆä¿æŒä½ åŽŸæœ‰çš„ Deep/Shallowï¼Œä½†æ›´ç²¾å‡†ï¼‰"""
        sig = BugAnalyzer.get_signature(error_msg).lower()
        
        if "segfault" in sig or "core_dump" in sig:
            return "CRITICAL_SEGFAULT"  # å•ç‹¬æŠŠå´©æºƒæ‹Žå‡ºæ¥
        
        deep_keywords = ['cuda', 'kernel', 'launch', 'cublas', 'cudnn', 'internal', 'assert']
        if any(k in sig for k in deep_keywords):
            return "DEEP_INTERNAL"
            
        shallow_keywords = ['type', 'shape', 'dim', 'expect', 'got', 'invalid', 'implement']
        if any(k in sig for k in shallow_keywords):
            return "SHALLOW_CHECK"
            
        return "RUNTIME_OTHER"

class BugTracker:
    def __init__(self, name: str, output_dir: str):
        self.name = name
        self.output_dir = output_dir
        
        # å…¼å®¹æ—§é€»è¾‘ï¼šå­˜å‚¨ç®€å•çš„åˆ—è¡¨ï¼Œç”¨äºŽç»˜å›¾å‡½æ•°çš„è®¡æ•°
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
        
        # ðŸ”¥ æ–°é€»è¾‘ï¼šå­˜å‚¨ç»“æž„åŒ–æŒ‡çº¹ä¿¡æ¯
        self.unique_bugs = defaultdict(list)
        self.bug_stats = defaultdict(int) # ç»Ÿè®¡å„ç±»åˆ«çš„æ•°é‡
        
    def scan_bugs(self):
        # æ¸…ç©ºé‡æ‰«ï¼Œé˜²æ­¢é‡å¤
        self.unique_bugs.clear()
        self.bug_stats.clear()
        # æ³¨æ„ï¼šä¸ºäº†ç»˜å›¾å…¼å®¹ï¼Œæˆ‘ä»¬ä¸è½»æ˜“æ¸…ç©º self.bugsï¼Œè€Œæ˜¯æ¯æ¬¡å¢žé‡æ·»åŠ æ–°çš„
        # æˆ–è€…ä¸ºäº†ä¿æŒä¸€è‡´ï¼Œè¿™é‡Œå…ˆä¸æ¸…ç©º self.bugsï¼Œä¾é  set åŽ»é‡
        
        oracle_map = {"crash": "crash-oracle", "cuda": "cuda-oracle", "precision": "precision-oracle"}
        
        for bug_type, oracle_name in oracle_map.items():
            bug_dir = join(self.output_dir, oracle_name, "potential-bug")
            if not os.path.exists(bug_dir):
                continue
                
            for root, _, files in os.walk(bug_dir):
                for f in files:
                    if not f.endswith('.py'): continue
                    
                    file_path = join(root, f)
                    
                    # 1. æ—§é€»è¾‘å…¼å®¹ï¼šåŠ å…¥åˆ—è¡¨ï¼Œç”¨äºŽç»˜å›¾ç»Ÿè®¡æ€»æ•°
                    if file_path not in self.bug_files[bug_type]:
                        self.bug_files[bug_type].add(file_path)
                        self.bugs[bug_type].append((len(self.bugs[bug_type]), "unknown", file_path))
                    
                    # 2. ðŸ”¥ æ–°é€»è¾‘ï¼šæŒ‡çº¹æå–ä¸ŽåŽ»é‡
                    try:
                        # å°è¯•è¯»å–é”™è¯¯æ—¥å¿—ï¼ˆå‡è®¾åŒå .txt æˆ– .log å­˜åœ¨ï¼Œæˆ–è€…ä»Ž py æ–‡ä»¶æ³¨é‡Šè¯»å–ï¼‰
                        # è¿™é‡Œç®€åŒ–ä¸ºï¼šç›´æŽ¥è¯»å– python æ–‡ä»¶ï¼Œå¦‚æžœé‡Œé¢æ²¡æœ‰é”™è¯¯ä¿¡æ¯ï¼Œé»˜è®¤æ ‡è®°
                        content = ""
                        with open(file_path, 'r', errors='ignore') as f_obj:
                            content = f_obj.read()
                        
                        # æå–æŒ‡çº¹
                        signature = BugAnalyzer.get_signature(content)
                        category = BugAnalyzer.classify_bug(content)
                        
                        # ç»„åˆé”®å€¼ï¼šç±»åž‹ + æŒ‡çº¹
                        unique_key = f"[{bug_type.upper()}]_[{category}] : {signature}"
                        
                        self.unique_bugs[unique_key].append(file_path)
                        self.bug_stats[category] += 1
                        
                    except Exception as e:
                        # å®¹é”™å¤„ç†
                        pass

    def get_total_bugs(self) -> int:
        return sum(len(bugs) for bugs in self.bugs.values())
    
    def get_bugs_by_type(self, bug_type: str) -> int:
        return len(self.bugs.get(bug_type, []))
    
    def print_summary(self):
        self.scan_bugs()
        print(f"\n{'='*70}")
        print(f"ðŸ§© BUG ANALYSIS REPORT: {self.name}")
        print(f"{'='*70}")
        
        # æ‰“å°åŸºäºŽæŒ‡çº¹çš„åŽ»é‡ç»Ÿè®¡
        print(f"Total Unique Issues: {len(self.unique_bugs)}")
        print(f"Distribution: {dict(self.bug_stats)}")
        print("-" * 70)
        
        # æ‰“å° Top 5 å”¯ä¸€ Bug
        print("Top Unique Bugs Found:")
        sorted_bugs = sorted(self.unique_bugs.items(), key=lambda x: len(x[1]), reverse=True)
        
        for i, (sig, files) in enumerate(sorted_bugs[:5]):
            print(f" {i+1}. [Count: {len(files)}] {sig}")
            # æ‰“å°ä¸€ä¸ªæ ·æœ¬è·¯å¾„
            rel_path = files[0].replace(self.output_dir + "/", "")
            print(f"    Sample: {rel_path}")
        
        if not sorted_bugs:
            print(" No bugs found.")
            
        # ä¿ç•™æ—§çš„ç»Ÿè®¡è¾“å‡ºï¼Œä½œä¸ºå¯¹æ¯”
        print("-" * 70)
        total_raw = self.get_total_bugs()
        total_unique = len(self.unique_bugs)
        print(f"📌 UNIQUE Bugs: {total_unique}")
        print(f"📄 Raw Files:   CRASH={self.get_bugs_by_type('crash')} | CUDA={self.get_bugs_by_type('cuda')} | PRECISION={self.get_bugs_by_type('precision')} | Total={total_raw}")
        print(f"📊 Dedup Rate:  {total_unique}/{total_raw} ({total_unique/max(total_raw,1)*100:.1f}% unique)")
        print(f"{'='*70}\n")


# =============================================================================
# ðŸ”¥ NEW: Adaptive Saturation Detector (åŠ¨æ€é¥±å’Œæ£€æµ‹å™¨)

# =============================================================================
# 🆕 RealTimeBugDeduplicator (实时 Bug 去重)
# =============================================================================

class RealTimeBugDeduplicator:
    """
    实时 Bug 去重器 - 基于错误签名去重
    
    解决问题：原始 BugTracker 读取 .py 文件内容，无法提取错误信息
    """
    
    CLEAN_PATTERNS = [
        (r'0x[0-9a-fA-F]+', 'ADDR'),
        (r'\d+\.\d+', 'FLOAT'),
        (r'(?<!\w)\d+(?!\w)', 'INT'),
        (r'\[.*?\]', '[SHAPE]'),
        (r'at .*?:\d+', 'at FILE:LINE'),
        (r'\s+', ' '),
    ]
    
    def __init__(self, max_signatures: int = 10000):
        self.max_signatures = max_signatures
        self.signatures: Dict[str, Set[str]] = {'crash': set(), 'cuda': set(), 'precision': set()}
        self.first_occurrence: Dict[str, dict] = {}
        self.total_bugs = {'crash': 0, 'cuda': 0, 'precision': 0}
        self.unique_bugs = {'crash': 0, 'cuda': 0, 'precision': 0}
    
    def get_signature(self, error_msg: str) -> str:
        if not error_msg:
            return "UNKNOWN"
        lines = error_msg.strip().split('\n')
        core_msg = lines[-1]
        for line in reversed(lines):
            if any(kw in line for kw in ['Error:', 'Exception:', 'INTERNAL ASSERT']):
                core_msg = line
                break
        clean_msg = core_msg
        for pattern, replacement in self.CLEAN_PATTERNS:
            clean_msg = re.sub(pattern, replacement, clean_msg)
        if 'Segmentation fault' in error_msg:
            return "SEGFAULT"
        return clean_msg.strip()[:200]
    
    def record_bug(self, oracle_type: str, error_msg: str, iteration: int = 0) -> Tuple[bool, str]:
        oracle_type = oracle_type.lower()
        if oracle_type not in self.signatures:
            oracle_type = 'crash'
        self.total_bugs[oracle_type] += 1
        signature = self.get_signature(error_msg)
        sig_hash = hashlib.md5(signature.encode()).hexdigest()[:12]
        if sig_hash in self.signatures[oracle_type]:
            return False, signature
        if len(self.signatures[oracle_type]) >= self.max_signatures:
            return False, signature
        self.signatures[oracle_type].add(sig_hash)
        self.unique_bugs[oracle_type] += 1
        self.first_occurrence[sig_hash] = {
            'oracle': oracle_type, 'signature': signature,
            'iteration': iteration, 'error': error_msg[:300]
        }
        return True, signature
    
    def get_dedup_stats(self) -> dict:
        return {
            'total': self.total_bugs.copy(),
            'unique': self.unique_bugs.copy(),
            'dedup_rate': {k: 1 - (self.unique_bugs[k] / max(self.total_bugs[k], 1)) for k in self.total_bugs}
        }
    
    def print_summary(self):
        stats = self.get_dedup_stats()
        print(f"\n{'='*70}")
        print("🔍 BUG DEDUPLICATION REPORT")
        print(f"{'='*70}")
        for oracle in ['crash', 'cuda', 'precision']:
            total, unique = stats['total'][oracle], stats['unique'][oracle]
            rate = stats['dedup_rate'][oracle] * 100
            print(f"[{oracle.upper()}] Total: {total}, Unique: {unique}, Dup Rate: {rate:.1f}%")
        print(f"\nTop Unique Signatures:")
        for i, (sig_hash, info) in enumerate(list(self.first_occurrence.items())[:10]):
            print(f"  {i+1}. [{info['oracle'].upper()}] {info['signature'][:60]}...")
        print(f"{'='*70}")


# =============================================================================
# 🆕 DispatcherSpace (参数组合覆盖率追踪)
# =============================================================================

class DispatcherSpace:
    """
    Dispatcher 状态空间追踪器 - 用于计算参数组合覆盖率
    
    计算原理：
    - 分母 (Denominator): 理论全集 = N_dtypes × N_devices × ...
    - 分子 (Numerator): 实际命中的参数组合（去重）
    - 覆盖率 = Numerator / Denominator
    
    内存优化：使用 MD5 哈希存储，限制最大记录数防止 OOM
    """
    
    DEFAULT_DIMENSIONS = {
        'dtype': ['float16', 'float32', 'float64', 'bfloat16',
                  'int8', 'int16', 'int32', 'int64', 'uint8',
                  'bool', 'complex64', 'complex128'],
        'device': ['cpu', 'cuda'],
    }
    
    def __init__(self, max_hits: int = 50000):
        self.max_hits = max_hits
        self.api_dimensions: Dict[str, Dict[str, List[str]]] = {}
        self.hits: Dict[str, Set[str]] = defaultdict(set)
        self.theoretical_sizes: Dict[str, int] = {}
        self.total_records = 0
        self.overflow_warnings = 0
    
    def register_api(self, api_name: str, dimensions: Dict[str, List[str]] = None):
        if dimensions is None:
            dimensions = self.DEFAULT_DIMENSIONS.copy()
        self.api_dimensions[api_name] = dimensions
        size = 1
        for dim_values in dimensions.values():
            size *= len(dim_values)
        self.theoretical_sizes[api_name] = size
        self.hits[api_name] = set()
        print(f"[DispatcherSpace] Registered: {api_name}, space={size}")
    
    def record_hit(self, api_name: str, api, is_cuda: bool = False) -> bool:
        """
        记录参数组合命中
        
        Args:
            api_name: API 名称
            api: TorchAPI 实例
            is_cuda: 是否在 CUDA 上执行
        """
        if api_name not in self.api_dimensions:
            self.register_api(api_name)
        if self.total_records >= self.max_hits:
            self.overflow_warnings += 1
            return False
        
        state_parts = []
        
        # 1. 提取 device
        device = "cuda" if is_cuda else "cpu"
        state_parts.append(f"dev={device}")
        
        # 2. 提取 dtype（从所有参数）
        dtypes_found = set()
        for param_name, arg in api.args.items():
            if arg is None:
                continue
            # Tensor 的 dtype
            if hasattr(arg, 'dtype') and arg.dtype is not None:
                dtype_str = str(arg.dtype).replace('torch.', '')
                dtypes_found.add(dtype_str)
            # 显式 dtype 参数
            elif hasattr(arg, 'value') and hasattr(arg, 'type'):
                if arg.type == ArgType.TORCH_DTYPE:
                    dtype_str = str(arg.value).replace('torch.', '')
                    dtypes_found.add(dtype_str)
        
        # 添加所有 dtype
        for dtype in sorted(dtypes_found):
            state_parts.append(f"d={dtype}")
        
        if len(state_parts) <= 1:  # 只有 device，没有 dtype
            return False
        
        # 生成哈希
        state_str = "|".join(sorted(state_parts))
        state_hash = hashlib.md5(state_str.encode()).hexdigest()[:12]
        
        if state_hash not in self.hits[api_name]:
            self.hits[api_name].add(state_hash)
            self.total_records += 1
            return True
        return False
    
    def get_coverage(self, api_name: str) -> float:
        if api_name not in self.theoretical_sizes:
            return 0.0
        actual = len(self.hits[api_name])
        theoretical = self.theoretical_sizes[api_name]
        return actual / theoretical if theoretical > 0 else 0.0
    
    def print_summary(self):
        print(f"\n{'='*70}")
        print("📊 DISPATCHER SPACE COVERAGE REPORT")
        print(f"{'='*70}")
        for api_name in self.api_dimensions:
            actual = len(self.hits[api_name])
            theoretical = self.theoretical_sizes[api_name]
            cov = self.get_coverage(api_name)
            bar_w, filled = 30, int(30 * cov)
            bar = '█' * filled + '░' * (bar_w - filled)
            print(f"[{api_name}] {actual}/{theoretical} ({cov*100:.1f}%) [{bar}]")
        print(f"Total: {self.total_records}, Overflow: {self.overflow_warnings}")
        print(f"{'='*70}")


# =============================================================================

class AdaptiveSaturationDetector:
    """
    åŠ¨æ€é¥±å’Œæ£€æµ‹å™¨ - ä¸åœæ­¢ï¼Œè€Œæ˜¯æ‰©å¤§æœç´¢èŒƒå›´
    
    ç­–ç•¥:
    1. è¿žç»­ N æ¬¡æ— å‘çŽ° â†’ è§¦å‘"æ‰©å¤§æœç´¢"è€Œéž"åœæ­¢"
    2. æ‰©å¤§æœç´¢ = æå‡æŽ¢ç´¢çŽ‡ + æ‰©å¤§å˜å¼‚èŒƒå›´
    3. å‘çŽ°æ–° Kernel â†’ ç«‹å³æ¢å¤æ­£å¸¸æ¨¡å¼
    """
    
    def __init__(self, 
                 patience: int = 500,           # ðŸ”§ å®¹å¿å¤šå°‘æ¬¡æ— æ–°å‘çŽ°
                 check_interval: int = 100):
        self.patience = patience
        self.check_interval = check_interval
        
        self.no_discovery_count = 0
        self.last_kernel_count = 0
        self.last_check_iteration = 0
        
        # æ‰©å¤§æœç´¢æ ‡å¿—
        self.expansion_mode = False
        self.expansion_count = 0
    
    def update(self, current_kernels: int, iteration: int) -> Tuple[bool, str]:
        """
        æ›´æ–°çŠ¶æ€å¹¶æ£€æŸ¥æ˜¯å¦éœ€è¦æ‰©å¤§æœç´¢
        
        Returns:
            (should_expand, message)
        """
        # æ£€æŸ¥æ˜¯å¦æœ‰æ–°å‘çŽ°
        if current_kernels > self.last_kernel_count:
            self.no_discovery_count = 0
            self.last_kernel_count = current_kernels
            
            # å‘çŽ°æ–° Kernelï¼Œé€€å‡ºæ‰©å±•æ¨¡å¼
            if self.expansion_mode:
                self.expansion_mode = False
                return False, "âœ… New kernels found! Returning to normal mode"
        else:
            self.no_discovery_count += 1
        
        # å®šæœŸæ£€æŸ¥
        if iteration - self.last_check_iteration >= self.check_interval:
            self.last_check_iteration = iteration
            
            # è§¦å‘æ‰©å¤§æœç´¢
            if self.no_discovery_count >= self.patience and not self.expansion_mode:
                self.expansion_mode = True
                self.expansion_count += 1
                return True, f"ðŸ” Expanding search (stagnation: {self.no_discovery_count} iters)"
        
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
    """è¦†ç›–çŽ‡è¿½è¸ªå™¨ + åŠ¨æ€é¥±å’Œæ£€æµ‹"""
    
    def __init__(self, name: str, enable_adaptive_saturation: bool = True):
        self.name = name
        self.all_kernels: Set[str] = set()
        self.kernel_provenance: Dict[str, int] = {}
        self.history: List[Tuple[int, int]] = []
        self.new_kernel_iterations: List[int] = []
        
        # åŠ¨æ€é¥±å’Œæ£€æµ‹
        self.saturation_detector = AdaptiveSaturationDetector() if enable_adaptive_saturation else None
    
    def update(self, new_kernels: Set[str], iteration: int) -> Tuple[int, Tuple[bool, str]]:
        """
        æ›´æ–°è¦†ç›–çŽ‡
        
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
        
        # åŠ¨æ€é¥±å’Œæ£€æµ‹
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
    """è¿›åŒ–ç§å­æ± """
    
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
# ðŸ”¥ NEW: Adaptive Mutation Controller (åŠ¨æ€å˜å¼‚æŽ§åˆ¶å™¨)
# =============================================================================

class AdaptiveMutationController:
    """
    åŠ¨æ€å˜å¼‚æŽ§åˆ¶å™¨
    
    åŠŸèƒ½:
    1. æ ¹æ®åœæ»žæƒ…å†µè‡ªåŠ¨è°ƒæ•´å˜å¼‚èŒƒå›´
    2. æ”¯æŒ Îµ-greedy æŽ¢ç´¢ç­–ç•¥
    3. å‘çŽ°æ–° Kernel æ—¶ç«‹å³æ¢å¤å¾®åˆ›æ¨¡å¼
    """
    
    def __init__(self, 
                 base_epsilon: float = 0.1,          # åŸºç¡€æŽ¢ç´¢çŽ‡
                 expansion_epsilon: float = 0.3,     # æ‰©å¼ æ¨¡å¼æŽ¢ç´¢çŽ‡
                 surgical_range: int = 8,            # å¾®åˆ›èŒƒå›´
                 exploration_range: int = 64):       # æŽ¢ç´¢èŒƒå›´
        self.base_epsilon = base_epsilon
        self.expansion_epsilon = expansion_epsilon
        self.surgical_range = surgical_range
        self.exploration_range = exploration_range
        
        # å½“å‰çŠ¶æ€
        self.current_epsilon = base_epsilon
        self.current_range = surgical_range
        self.expansion_mode = False
        
        # ç»Ÿè®¡
        self.exploration_count = 0
        self.exploitation_count = 0
    
    def should_explore(self) -> bool:
        """å†³å®šæœ¬æ¬¡è¿­ä»£æ˜¯å¦é‡‡ç”¨æŽ¢ç´¢æ¨¡å¼"""
        if random.random() < self.current_epsilon:
            self.exploration_count += 1
            return True
        else:
            self.exploitation_count += 1
            return False
    
    def enter_expansion_mode(self):
        """è¿›å…¥æ‰©å¼ æ¨¡å¼ï¼ˆåœæ»žæ—¶è§¦å‘ï¼‰"""
        self.expansion_mode = True
        self.current_epsilon = self.expansion_epsilon
        self.current_range = self.exploration_range
        print(f"  ðŸ” [Mutation] Expansion mode: Îµ={self.current_epsilon}, range=Â±{self.current_range}")
    
    def exit_expansion_mode(self):
        """é€€å‡ºæ‰©å¼ æ¨¡å¼ï¼ˆå‘çŽ°æ–° Kernel æ—¶ï¼‰"""
        self.expansion_mode = False
        self.current_epsilon = self.base_epsilon
        self.current_range = self.surgical_range
        print(f"  âœ… [Mutation] Normal mode: Îµ={self.current_epsilon}, range=Â±{self.current_range}")
    
    def get_mutation_range(self) -> int:
        """èŽ·å–å½“å‰å˜å¼‚èŒƒå›´"""
        return self.current_range
    
    def get_status(self) -> str:
        total = self.exploration_count + self.exploitation_count
        if total == 0:
            return "No mutations yet"
        explore_pct = self.exploration_count / total * 100
        return (f"Explore: {self.exploration_count}/{total} ({explore_pct:.1f}%) | "
                f"Mode: {'Expansion' if self.expansion_mode else 'Normal'} | "
                f"Îµ={self.current_epsilon:.2f}, range=Â±{self.current_range}")


# =============================================================================
# Probability Patcher
# =============================================================================

class ProbabilityPatcher:
    """å°†æ•°æ®åº“é‡‡æ ·æ¦‚çŽ‡ä»Ž 20% æå‡åˆ° 80%"""
    
    @staticmethod
    def patch_high_db_probability():
        import utils.probability as prob_module
        
        global _ORIGINAL_DO_SELECT_FROM_DB
        _ORIGINAL_DO_SELECT_FROM_DB = prob_module.do_select_from_db
        
        def high_db_select() -> bool:
            from numpy.random import rand
            return rand() < 0.5
        
        prob_module.do_select_from_db = high_db_select
        print("[Patch] âœ… Database sampling: 20% â†’ 80%")
    
    @staticmethod
    def restore():
        if _ORIGINAL_DO_SELECT_FROM_DB:
            import utils.probability as prob_module
            prob_module.do_select_from_db = _ORIGINAL_DO_SELECT_FROM_DB
            print("[Patch] ðŸ”„ Database sampling restored")


# =============================================================================
# ðŸ§ª NEW: Poison Patcher (æŠ•æ¯’è¡¥ä¸ - ç‹¬ç«‹äºŽç­–ç•¥)
# =============================================================================

# ä¿å­˜åŽŸå§‹æ–¹æ³•çš„å…¨å±€å˜é‡
_POISON_ORIGINAL_FLOAT = None
_POISON_ORIGINAL_INT = None

class PoisonPatcher:
    """
    ç‹¬ç«‹çš„æŠ•æ¯’è¡¥ä¸ - å¯¹ Random å’Œ Guided éƒ½ç”Ÿæ•ˆ
    
    æµ®ç‚¹æŠ•æ¯’:
    - 5%:  Infinity (Â±âˆž)
    - 5%:  NaN
    - 10%: Extreme Values [1e20, -1e20, 1e-10, -1e-10]
    - 30%: å­—å…¸é‡‡æ ·
    - 50%: æ¸©å’Œå¾®è°ƒ
    
    æ•´æ•°æŠ•æ¯’:
    - 10%: è¾¹ç•Œå€¼ [0, -1, 1]
    - 10%: æžç«¯å€¼ [-999, 999, Â±2^31]
    - 10%: é™·é˜±å€¼ [-2, -3, 256, 512, è´¨æ•°]
    - 30%: å­—å…¸é‡‡æ ·
    - 40%: æ¸©å’Œå¾®è°ƒ
    """
    
    @staticmethod
    def patch():
        global _POISON_ORIGINAL_FLOAT, _POISON_ORIGINAL_INT
        
        _POISON_ORIGINAL_FLOAT = Argument.mutate_float_value
        _POISON_ORIGINAL_INT = Argument.mutate_int_value
        
        def poison_float_mutation(self, value) -> float:
            """ðŸ§ª Float Poison Injection - å¯¹æ‰€æœ‰ç­–ç•¥ç”Ÿæ•ˆ"""
            from numpy.random import rand, choice
            
            roll = rand()
            
            # [5%] æ³¨å…¥ Infinity (æ­£/è´Ÿæ— ç©·)
            if roll < 0.05:
                return choice([float('inf'), float('-inf')])
            
            # [5%] æ³¨å…¥ NaN
            elif roll < 0.10:
                return float('nan')
            
            # [10%] æ³¨å…¥æžç«¯å€¼ (Extreme Values)
            elif roll < 0.20:
                extreme_values = [1e20, -1e20, 1e-10, -1e-10]
                return choice(extreme_values)
            
            # [30%] åŽŸå§‹é€»è¾‘ - å­—å…¸é‡‡æ ·
            elif roll < 0.50:
                return choice(Argument._float_values)
            
            # [50%] åŽŸå§‹é€»è¾‘ - æ¸©å’Œå¾®è°ƒ
            else:
                return value + (rand() - 0.5) * 8.0
        
        def poison_int_mutation(self, value, _min=None, _max=None) -> int:
            """ðŸ§ª Int Poison Injection - å¯¹æ‰€æœ‰ç­–ç•¥ç”Ÿæ•ˆ"""
            from numpy.random import rand, choice, randint
            
            roll = rand()
            
            # [10%] è¾¹ç•Œå€¼ - æœ€å®¹æ˜“è§¦å‘é€»è¾‘é”™è¯¯
            if roll < 0.10:
                boundary_values = [0, -1, 1]
                new_value = choice(boundary_values)
            
            # [10%] æžç«¯å€¼ - æº¢å‡ºå’Œè¾¹ç•Œæ£€æŸ¥
            elif roll < 0.20:
                extreme_values = [-999, 999, -2147483648, 2147483647, -65536, 65536]
                new_value = choice(extreme_values)
            
            # [10%] å¸¸è§é™·é˜±å€¼ - ç‰¹å®šå‚æ•°çš„é—®é¢˜å€¼
            elif roll < 0.30:
                trap_values = [
                    -2, -3, -4,      # è´Ÿæ•°ç»´åº¦
                    256, 512, 1024,  # å¤§å°ºå¯¸
                    7, 11, 13,       # è´¨æ•° (ä¸èƒ½æ•´é™¤)
                    0,               # é‡å¤å¼ºè°ƒ 0
                ]
                new_value = choice(trap_values)
            
            # [30%] å­—å…¸é‡‡æ ·
            elif roll < 0.60:
                new_value = choice(Argument._int_values)
            
            # [40%] æ¸©å’Œå¾®è°ƒ
            else:
                new_value = value + randint(-8, 9)
            
            # åº”ç”¨è¾¹ç•Œé™åˆ¶ (ä½†ä¿ç•™ -1 ç­‰ç‰¹æ®Šå€¼ç”¨äºŽè§¦å‘ bug)
            if _min is not None and new_value < _min and new_value not in [-1, 0]:
                new_value = max(_min, new_value)
            if _max is not None and new_value > _max:
                new_value = min(_max, new_value)
            
            return int(new_value)
        
        # ä¿®æ­£ï¼šå‡½æ•°åè¦å¯¹åº”ä¸Šé¢å®šä¹‰çš„ poion_float_mutation
        Argument.mutate_float_value = poison_float_mutation 
        Argument.mutate_int_value = poison_int_mutation
        print("[Patch] ðŸ§ª Poison Injection enabled (ALL strategies):")
        print("        Float: 5% Inf + 5% NaN + 10% Extreme")
        print("        Int:   10% boundary + 10% extreme + 10% trap")
    
    @staticmethod
    def restore():
        global _POISON_ORIGINAL_FLOAT, _POISON_ORIGINAL_INT
        if _POISON_ORIGINAL_FLOAT:
            Argument.mutate_float_value = _POISON_ORIGINAL_FLOAT
        if _POISON_ORIGINAL_INT:
            Argument.mutate_int_value = _POISON_ORIGINAL_INT
        print("[Patch] ðŸ”„ Poison Injection restored")


# =============================================================================
# ðŸ”¥ NEW: Adaptive Mutation Patcher (åŠ¨æ€å˜å¼‚è¡¥ä¸ - ä»… Guided)
# =============================================================================

class AdaptiveMutationPatcher:
    """åŠ¨æ€èŒƒå›´å˜å¼‚è¡¥ä¸ - ä»… Guided ç­–ç•¥ä½¿ç”¨ï¼ŒæŠ•æ¯’ç”± PoisonPatcher ç»Ÿä¸€å¤„ç†"""
    
    @staticmethod
    def patch_adaptive_mutation(controller: AdaptiveMutationController):
        """
        Guided ç­–ç•¥é¢å¤–ä½¿ç”¨åŠ¨æ€èŒƒå›´è°ƒæ•´
        æ³¨æ„: åŸºç¡€æŠ•æ¯’å·²ç”± PoisonPatcher å¤„ç†ï¼Œè¿™é‡Œåªå¢žåŠ åŠ¨æ€èŒƒå›´åŠŸèƒ½
        """
        # æ³¨æ„: ä¸å†ä¿å­˜/è¦†ç›–åŽŸå§‹æ–¹æ³•ï¼Œå› ä¸º PoisonPatcher å·²ç»å¤„ç†äº†
        # è¿™ä¸ª patcher çŽ°åœ¨åªæ˜¯ä¸€ä¸ªæ ‡è®°ï¼Œè¡¨ç¤º Guided ç­–ç•¥å¯ç”¨äº†åŠ¨æ€èŒƒå›´
        print(f"[Patch] âœ… Adaptive range enabled for Guided: Â±{controller.get_mutation_range()}")
    
    @staticmethod
    def restore():
        # PoisonPatcher ä¼šè´Ÿè´£æ¢å¤ï¼Œè¿™é‡Œåªæ‰“å°ä¿¡æ¯
        print("[Patch] ðŸ”„ Adaptive range disabled")


# =============================================================================
# ðŸ”¥ Enhanced Fuzzer with Hybrid Strategy
# =============================================================================

class EnhancedFuzzer:
    """æ”¯æŒæ··åˆç­–ç•¥çš„å¢žå¼ºåž‹ Fuzzer"""
    
    def __init__(self, 
                 api_name: str, 
                 output_dir: str, 
                 strategy_name: str, 
                 enable_patches: bool,
                 use_all_oracles: bool = True,
                 enable_logging: bool = True,
                 enable_checkpoint: bool = True,
                 enable_safety_guards: bool = True,
                 diff_bound: float = 1e-5,
                 warmup_ratio: float = 0.1,           # 🆕 热启动比例
                 enable_dispatcher: bool = True):     # 🆕 启用 DispatcherSpace  # ðŸ”§
        self.api_name = api_name
        self.output_dir = output_dir
        self.strategy_name = strategy_name
        self.enable_patches = enable_patches
        self.use_all_oracles = use_all_oracles
        self.enable_logging = enable_logging
        self.enable_checkpoint = enable_checkpoint
        self.enable_safety_guards = enable_safety_guards
        self.diff_bound = diff_bound
        self.warmup_ratio = warmup_ratio             # 🆕 保存热启动比例
        self.enable_dispatcher = enable_dispatcher   # 🆕 保存dispatcher开关
        
        # Trackers
        self.coverage = EnhancedCoverageTracker(strategy_name, enable_adaptive_saturation=enable_patches)
        self.bug_tracker = BugTracker(strategy_name, output_dir)
        
        # Guided ä¸“å±ž
        self.corpus = EvolutionaryCorpus(max_size=100) if enable_patches else None
        self.mutation_controller = AdaptiveMutationController() if enable_patches else None
        
        # Library - ä½¿ç”¨æ›´ä¸¥æ ¼çš„ diff_bound é…åˆæŠ•æ¯’ç­–ç•¥
        self.library = TorchLibrary(output_dir, diff_bound=diff_bound)
        print(f"[Fuzzer] ðŸŽ¯ Precision tolerance: diff_bound={diff_bound}")
        
        # Oracle åˆ—è¡¨
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
            self.outlier_filter = OutlierFilter(max_elements=int(5e6), max_memory_gb=2.0)  # 🔧 降低限制防止OOM
            print(f"[Safety] Guards enabled: Speedometer + DiskGuard + OutlierFilter")
        
        # 🆕 DispatcherSpace 初始化
        self.dispatcher_space = None
        if enable_dispatcher:
            self.dispatcher_space = DispatcherSpace(max_hits=50000)
            self.dispatcher_space.register_api(api_name)
        
        # 🆕 实时 Bug 去重器
        self.bug_deduplicator = RealTimeBugDeduplicator(max_signatures=10000)
        
        # 🆕 Warmup 配置 (阈值在 run_fuzzing_loop 中计算)
        self.warmup_threshold = 0
        
        print(f"\n[Fuzzer] Initialized: {strategy_name}")
        print(f"  API: {api_name}")
        print(f"  Patches: {'Enabled' if enable_patches else 'Disabled'}")
        print(f"  Hybrid Strategy: {'Active' if self.mutation_controller else 'N/A'}")
        print(f"  Data Logging: {'Enabled' if enable_logging else 'Disabled'}")
        print(f"  Checkpoint: {'Enabled' if enable_checkpoint else 'Disabled'}")
        print(f"  Safety Guards: {'Enabled' if enable_safety_guards else 'Disabled'}")
        print(f"  Warmup Ratio: {warmup_ratio*100:.0f}%")
        print(f"  DispatcherSpace: {'Enabled' if enable_dispatcher else 'Disabled'}")
    
    def run_fuzzing_loop(self, 
                         max_iterations: int = 10000,
                         checkpoint_interval: int = 100,
                         bug_scan_interval: int = 50):
        """
        ä¸» Fuzzing å¾ªçŽ¯ - æ··åˆç­–ç•¥ç‰ˆæœ¬
        """
        # ====================================================================
        # åˆå§‹åŒ– Safety Guards
        # ====================================================================
        if self.speedometer:
            self.speedometer.start()
        
        # ====================================================================
        # å°è¯•ä»Ž checkpoint æ¢å¤
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
                
                print(f"\nâœ… Resuming from iteration {start_iteration}")
                print(f"  Previous kernels: {len(self.coverage.all_kernels)}")
                if self.corpus:
                    print(f"  Previous corpus: {len(self.corpus.corpus)} seeds")
                print(f"{'='*70}\n")
        
        # ====================================================================
        # ä¸»å¾ªçŽ¯
        # ====================================================================
        print(f"\n{'='*70}")
        print(f"Starting {self.strategy_name} fuzzing")
        if self.mutation_controller:
            print(f"Hybrid Strategy: Îµ-greedy + Adaptive Mutation")
        print(f"Iterations: {start_iteration} â†’ {max_iterations}")
        if start_iteration > 0:
            print(f"(Resuming from checkpoint)")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        last_bug_count = 0
        
        # 🆕 计算热启动阈值
        self.warmup_threshold = int(max_iterations * self.warmup_ratio)
        print(f"🔥 Warmup Phase: iterations 0 ~ {self.warmup_threshold} (Random only)")
        print(f"🚀 Evolution Phase: iterations {self.warmup_threshold} ~ {max_iterations}")
        
        for i in range(start_iteration, max_iterations):
            # ================================================================
            # Speedometer tick
            # ================================================================
            if self.speedometer:
                self.speedometer.tick()
            
            # ================================================================
            # ðŸ”¥ æ··åˆç­–ç•¥ï¼šÎµ-greedy é€‰æ‹©
            # ================================================================
            source = ""
            is_exploration = False
            
            # 🆕 Phase 1: Warm-up (强制 Random)
            if i < self.warmup_threshold:
                api = TorchAPI(self.api_name)
                source = "warmup_random"
                api.mutate()
                if i == self.warmup_threshold - 1:
                    print(f"\n🚀 PHASE TRANSITION: Warm-up → Evolution (iter {i+1})")
            
            # 🆕 Phase 2: Evolution (ε-greedy)
            else:
                if self.mutation_controller:
                    is_exploration = self.mutation_controller.should_explore()
                
                if is_exploration:
                    api = TorchAPI(self.api_name)
                    source = "exploration"
                elif self.corpus and self.corpus.size() > 0 and random.random() < 0.7:
                    parent_api = self.corpus.select_parent()
                    api = copy.deepcopy(parent_api)
                    source = "corpus"
                else:
                    api = TorchAPI(self.api_name)
                    source = "random"
                api.mutate()
            
            # OutlierFilter æ£€æŸ¥
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
            # æµ‹è¯•æ‰€æœ‰ Oracle
            # ================================================================
            all_captured_kernels = set()
            execution_valid = False
            
            for oracle in self.oracles:
                try:
                    # 🆕 test_with_oracle 现在返回 (kernels, bug_info)
                    result = self.library.test_with_oracle(api, oracle)
                    
                    # 兼容旧版本（只返回 kernels）和新版本（返回元组）
                    if isinstance(result, tuple):
                        captured_kernels, bug_info = result
                    else:
                        captured_kernels, bug_info = result, None
                    
                    all_captured_kernels.update(captured_kernels)
                    execution_valid = True
                    
                    # 🆕 实时去重记录
                    if bug_info and hasattr(self, 'bug_deduplicator'):
                        is_new, sig = self.bug_deduplicator.record_bug(
                            oracle_type=bug_info.get('type', 'crash'),
                            error_msg=bug_info.get('error', ''),
                            iteration=i
                        )
                        if is_new:
                            print(f"  🐛 NEW [{bug_info.get('oracle', 'BUG')}]: {sig[:50]}...")
                            
                except Exception as e:
                    pass
            
            # è®°å½•åŽŸå§‹æ•°æ®
            if self.logger:
                self.logger.log_iteration(
                    iteration=i,
                    source=source,
                    api=api,
                    valid=execution_valid,
                    kernels=list(all_captured_kernels)
                )
            
            # 🆕 记录 DispatcherSpace 命中
            if self.dispatcher_space and execution_valid:
                # 检测是否使用了 CUDA (CUDA oracle 或代码中有 .cuda())
                is_cuda = OracleType.CUDA in self.oracles
                self.dispatcher_space.record_hit(self.api_name, api, is_cuda=is_cuda)
            
            # ================================================================
            # æ›´æ–°è¦†ç›–çŽ‡ + åŠ¨æ€é¥±å’Œæ£€æµ‹
            # ================================================================
            new_count, (should_expand, expansion_msg) = self.coverage.update(all_captured_kernels, i)
            
            # å“åº”æ‰©å¼ ä¿¡å·
            if should_expand and self.mutation_controller:
                self.mutation_controller.enter_expansion_mode()
            
            # å‘çŽ°æ–° Kernel æ—¶é€€å‡ºæ‰©å¼ æ¨¡å¼
            if new_count > 0 and self.mutation_controller:
                if self.mutation_controller.expansion_mode:
                    self.mutation_controller.exit_expansion_mode()
            
            # æ›´æ–° Corpus
            if new_count > 0 and self.corpus:
                self.corpus.add_seed(api, all_captured_kernels)
            
            # å®šæœŸæ‰«æ Bug
            if (i + 1) % bug_scan_interval == 0:
                prev_bug_count = self.bug_tracker.get_total_bugs()
                self.bug_tracker.scan_bugs()
                new_bugs = self.bug_tracker.get_total_bugs() - prev_bug_count
                
                if new_bugs > 0:
                    print(f"  ðŸ› [{self.strategy_name}] Found {new_bugs} new bugs! "
                          f"Total: {self.bug_tracker.get_total_bugs()}")
            
            # ================================================================
            # Checkpoint + Safety Guards
            # ================================================================
            if (i + 1) % checkpoint_interval == 0:
                # Checkpoint ä¿å­˜
                if self.checkpoint_manager:
                    self.checkpoint_manager.save(
                        iteration=i,
                        coverage_kernels=self.coverage.all_kernels,
                        corpus_seeds=self.corpus.corpus if self.corpus else None,
                        logger_iterations=self.logger.total_iterations if self.logger else 0
                    )
                
                # ç£ç›˜ç©ºé—´æ£€æŸ¥
                if self.disk_guard:
                    is_critical, message = self.disk_guard.check_and_cleanup()
                    if is_critical:
                        print(f"\n{message}")
                        print(f"âŒ STOPPING: Critical disk space issue")
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
                
                # Speedometer çŠ¶æ€
                if self.speedometer:
                    print(f"Speed: {self.speedometer.get_status(i, max_iterations)}")
                    is_slow, warning = self.speedometer.check_speed()
                    if is_slow:
                        print(warning)
                
                # Disk çŠ¶æ€
                if self.disk_guard:
                    print(f"Disk: {self.disk_guard.get_status()}")
                
                # OutlierFilter çŠ¶æ€
                if self.outlier_filter:
                    print(f"Filter: {self.outlier_filter.get_status()}")
                
                # Corpus çŠ¶æ€
                if self.corpus:
                    print(f"Corpus: {self.corpus.size()} seeds")
                
                # 🆕 DispatcherSpace 状态
                if self.dispatcher_space:
                    cov = self.dispatcher_space.get_coverage(self.api_name)
                    hits = len(self.dispatcher_space.hits[self.api_name])
                    print(f"Dispatcher: {hits} combos ({cov*100:.1f}% coverage)")
                
                # ðŸ”¥ Mutation Controller çŠ¶æ€
                if self.mutation_controller:
                    print(f"Mutation: {self.mutation_controller.get_status()}")
                
                # 🔧 定期清理内存防止 OOM (Exit 137)
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                # Bug æ‰«æ
                self.bug_tracker.scan_bugs()
        
        # ====================================================================
        # å®ŒæˆåŽæ¸…ç†
        # ====================================================================
        if self.checkpoint_manager:
            self.checkpoint_manager.clear()
        
        # æœ€ç»ˆç»Ÿè®¡
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
        
        # 🆕 DispatcherSpace 最终报告
        if self.dispatcher_space:
            self.dispatcher_space.print_summary()
        
        # 🆕 Bug 去重报告
        if hasattr(self, 'bug_deduplicator'):
            self.bug_deduplicator.print_summary()
        
        print(f"{'='*70}")
        
        return self.coverage
    
    def print_stats(self):
        """æ‰“å°ç»Ÿè®¡ä¿¡æ¯"""
        print(f"\n{'='*70}")
        print(f"FINAL STATISTICS: {self.strategy_name}")
        print(f"{'='*70}")
        print(f"Total Kernels: {self.coverage.get_total()}")
        
        # Bug ç»Ÿè®¡
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
    output_dir: str,
    random_dispatcher: DispatcherSpace = None,  # 🆕
    guided_dispatcher: DispatcherSpace = None,  # 🆕
    random_dedup = None,  # 🆕 Bug 去重器
    guided_dedup = None   # 🆕
):
    """ç»˜åˆ¶å®Œæ•´çš„ç»“æžœå¯¹æ¯”å›¾ï¼ˆåŒ…å« Bug ç»Ÿè®¡ï¼‰"""
    
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # Kernel è¦†ç›–çŽ‡æ›²çº¿
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
    
    # Bug æ•°é‡å¯¹æ¯”
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
    
    # æ€» Bug æ•°å¯¹æ¯”
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
    
    # å‘çŽ°é€ŸçŽ‡
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
    
    # ç»Ÿè®¡è¡¨
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.axis('off')
    
    # 🆕 获取 Dispatcher 覆盖率
    random_disp_cov = random_dispatcher.get_coverage(api_name) * 100 if random_dispatcher else 0
    guided_disp_cov = guided_dispatcher.get_coverage(api_name) * 100 if guided_dispatcher else 0
    
    # 🆕 获取去重后的 Bug 数量
    random_unique = sum(random_dedup.unique_bugs.values()) if random_dedup else random_bugs.get_total_bugs()
    guided_unique = sum(guided_dedup.unique_bugs.values()) if guided_dedup else guided_bugs.get_total_bugs()
    
    # 🆕 计算去重后的 Bug 数
    random_bugs.scan_bugs()
    guided_bugs.scan_bugs()
    random_unique = len(random_bugs.unique_bugs)
    guided_unique = len(guided_bugs.unique_bugs)
    
    table_data = [
        ["Metric", "Random", "Guided", "Ratio"],
        ["", "", "", ""],
        ["Kernels", 
         f"{random_coverage.get_total()}",
         f"{guided_coverage.get_total()}",
         f"{guided_coverage.get_total()/max(random_coverage.get_total(),1):.2f}x"],
        ["Dispatcher Cov",
         f"{random_disp_cov:.1f}%",
         f"{guided_disp_cov:.1f}%",
         f"{guided_disp_cov/max(random_disp_cov,0.1):.2f}x"],
        ["Unique Bugs",
         f"{random_unique}",
         f"{guided_unique}",
         f"{guided_unique/max(random_unique,1):.2f}x"],
        ["Raw Triggers",
         f"{random_bugs.get_total_bugs()}",
         f"{guided_bugs.get_total_bugs()}",
         f"{guided_bugs.get_total_bugs()/max(random_bugs.get_total_bugs(),1):.2f}x"],
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
    
    # æ€»æ ‡é¢˜
    fig.suptitle(
        f"Hybrid Strategy Benchmark: {api_name}\n"
        f"Îµ-greedy (10% Exploration) + Adaptive Mutation + Dynamic Saturation",
        fontsize=15, fontweight='bold', y=0.98
    )
    
    plt.tight_layout()
    
    plot_file = join(output_dir, f"{api_name.replace('.', '_')}_hybrid_strategy.png")
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\nðŸ“Š Hybrid strategy plot saved: {plot_file}")


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
    """è¿è¡Œå®Œæ•´çš„æ··åˆç­–ç•¥å®žéªŒ (å«æŠ•æ¯’ç­–ç•¥)"""
    os.makedirs(output_dir, exist_ok=True)
    
    # é…ç½®æ•°æ®åº“
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
        print("âŒ Config file not found")
        return None
    
    print(f"ðŸ“ Config: {os.path.abspath(config_path)}")
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
    # ðŸ§ª Enable Poison Injection for ALL strategies
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
        
        # ðŸ”¥ åº”ç”¨åŠ¨æ€å˜å¼‚è¡¥ä¸ (ä»… Guided)
        AdaptiveMutationPatcher.patch_adaptive_mutation(guided_fuzzer.mutation_controller)
        
        guided_coverage = guided_fuzzer.run_fuzzing_loop(
            max_iterations=max_iterations,
            checkpoint_interval=max(100, max_iterations // 20),
            bug_scan_interval=50
        )
        guided_fuzzer.print_stats()
        
    finally:
        # æ¢å¤æ‰€æœ‰è¡¥ä¸
        ProbabilityPatcher.restore()
        AdaptiveMutationPatcher.restore()
        PoisonPatcher.restore()
    
    # =========================================================================
    # Visualization
    # =========================================================================
    plot_full_oracle_results(
        random_coverage, guided_coverage,
        random_fuzzer.bug_tracker, guided_fuzzer.bug_tracker,
        api_name, output_dir,
        random_dispatcher=random_fuzzer.dispatcher_space,  # 🆕
        guided_dispatcher=guided_fuzzer.dispatcher_space,  # 🆕
        random_dedup=getattr(random_fuzzer, 'bug_deduplicator', None),  # 🆕
        guided_dedup=getattr(guided_fuzzer, 'bug_deduplicator', None)   # 🆕
    )
    
    # =========================================================================
    # Save Results
    # =========================================================================
    # 🆕 获取去重统计
    random_dedup_stats = random_fuzzer.bug_deduplicator.get_dedup_stats() if hasattr(random_fuzzer, 'bug_deduplicator') else None
    guided_dedup_stats = guided_fuzzer.bug_deduplicator.get_dedup_stats() if hasattr(guided_fuzzer, 'bug_deduplicator') else None
    
    results = {
        "api": api_name,
        "max_iterations": max_iterations,
        "hybrid_strategy": {
            "epsilon_greedy": "10% exploration",
            "adaptive_mutation": "Â±8 â†’ Â±64 on stagnation",
            "dynamic_saturation": "expand search instead of stop"
        },
        "random": {
            "total_kernels": random_coverage.get_total(),
            "iterations_run": len(random_coverage.history),
            "dispatcher_coverage": random_fuzzer.dispatcher_space.get_coverage(api_name) if random_fuzzer.dispatcher_space else 0,
            "bugs": {
                "total_triggers": random_fuzzer.bug_tracker.get_total_bugs(),
                "unique_bugs": sum(random_dedup_stats['unique'].values()) if random_dedup_stats else 0,
                "crash": random_fuzzer.bug_tracker.get_bugs_by_type("crash"),
                "cuda": random_fuzzer.bug_tracker.get_bugs_by_type("cuda"),
                "precision": random_fuzzer.bug_tracker.get_bugs_by_type("precision")
            }
        },
        "guided": {
            "total_kernels": guided_coverage.get_total(),
            "iterations_run": len(guided_coverage.history),
            "dispatcher_coverage": guided_fuzzer.dispatcher_space.get_coverage(api_name) if guided_fuzzer.dispatcher_space else 0,
            "bugs": {
                "total_triggers": guided_fuzzer.bug_tracker.get_total_bugs(),
                "unique_bugs": sum(guided_dedup_stats['unique'].values()) if guided_dedup_stats else 0,
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
    
    print(f"\nðŸ’¾ Results saved: {result_file}")
    
    return results


# =============================================================================
# Main
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Hybrid Strategy Benchmark: Îµ-greedy + Adaptive Mutation + Poison Injection"
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
    print("ðŸ”¬ HYBRID STRATEGY BENCHMARK + POISON INJECTION")
    print("="*70)
    print(f"API: {args.api}")
    print(f"Max Iterations: {args.max_iterations:,}")
    print(f"Strategy: Îµ-greedy (10% exploration) + Adaptive Mutation")
    print(f"ðŸ§ª Poison Injection: 5% Inf + 5% NaN + 10% Extreme")
    print(f"ðŸŽ¯ Precision Tolerance: {args.diff_bound}")
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