"""
torch_library.py - 修复版本
==========================
修复内容:
1. 添加 error_message 去重机制，避免同一 Bug 重复写入 1400+ 次
"""

from classes.torch_api import *
from classes.library import Library
from classes.argument import *
from classes.api import *
from os.path import join
import os
from constants.keys import *
import torch
from torch.profiler import profile, ProfilerActivity

class TorchLibrary(Library):
    def __init__(self, output_dir, diff_bound=1e-5, time_bound=10, time_thresold=1e-3) -> None:
        super().__init__(output_dir)
        self.diff_bound = diff_bound
        self.time_bound = time_bound
        self.time_thresold = time_thresold
        
        # =========================================================
        # [FIX-1] Bug 去重：内存中的 error_message 集合
        # =========================================================
        self._seen_errors = set()  # 已发现的错误信息
        self._dedup_stats = {"total": 0, "skipped": 0}  # 统计信息
    
    def _is_duplicate_bug(self, error_msg: str, bug_type: str) -> bool:
        """
        检查是否为重复 Bug
        
        Args:
            error_msg: 错误信息字符串
            bug_type: Bug 类型 (crash/cuda/precision)
        
        Returns:
            True 如果是重复 Bug，应跳过写入
        """
        if error_msg is None:
            return False
        
        # 创建去重 key：bug_type + error_msg 的前 200 字符
        # 截断是为了处理带有动态内容的错误信息
        dedup_key = f"{bug_type}:{error_msg[:200]}"
        
        self._dedup_stats["total"] += 1
        
        if dedup_key in self._seen_errors:
            self._dedup_stats["skipped"] += 1
            return True
        
        self._seen_errors.add(dedup_key)
        return False
    
    def get_dedup_stats(self) -> dict:
        """获取去重统计"""
        return self._dedup_stats.copy()
    
    def test_with_oracle(self, api: TorchAPI, oracle: OracleType):
        captured_kernels = set()
        
        if oracle == OracleType.CRASH:
            code = "import torch\n"
            code += self.generate_code(api, oracle)
            with open(join(self.directory, "temp.py"), "w") as f:
                f.write(code)
            
            _, error, kernels = self.run_code(code)
            if kernels: 
                captured_kernels.update(kernels)
            
            if error == None:
                self.write_to_dir(join(self.output[oracle], "success"), api.api, code)
            elif self.is_crash_msg(error):
                # =========================================================
                # [FIX-1] 去重检查：跳过重复的 crash bug
                # =========================================================
                if not self._is_duplicate_bug(error, "crash"):
                    self.write_to_dir(join(self.output[oracle], "potential-bug"), api.api, code)
            else:
                self.write_to_dir(join(self.output[oracle], "fail"), api.api, code)
                
        elif oracle == OracleType.CUDA:
            code = "import torch\n"
            code += api.to_code(res=f"{RES_KEY}[\"{RES_CPU_KEY}\"]", use_try=True, error_res=f"{RES_KEY}[\"{ERR_CPU_KEY}\"]")
            code += api.to_diff_code(oracle, res=f"{RES_KEY}[\"{RES_GPU_KEY}\"]", use_try=True, error_res=f"{RES_KEY}[\"{ERR_GPU_KEY}\"]")

            write_code = "results = dict()\n" + code + "\nprint(results)\n"
            with open(join(self.directory, "temp.py"), "w") as f:
                f.write(write_code)

            results, error, kernels = self.run_code(code)
            if kernels: 
                captured_kernels.update(kernels)

            write_dir = ""
            is_potential_bug = False
            bug_signature = None  # 用于去重的签名
            
            if error == None:
                if results[ERR_CPU_KEY] == None and results[ERR_GPU_KEY] == None:
                    try:
                        is_equal = self.is_equal(results[RES_CPU_KEY], results[RES_GPU_KEY], self.diff_bound)
                    except Exception as e:
                        write_dir = join(self.output[oracle], "compare-bug")
                        is_potential_bug = True
                        bug_signature = f"compare-exception:{str(e)[:100]}"
                    else:
                        if is_equal:
                            write_dir = join(self.output[oracle], "success")
                        else:
                            write_dir = join(self.output[oracle], "potential-bug")
                            is_potential_bug = True
                            bug_signature = "cpu-gpu-mismatch"
                elif self.is_crash_msg(results[ERR_CPU_KEY]) or self.is_crash_msg(results[ERR_GPU_KEY]):
                    write_dir = join(self.output[oracle], "potential-bug")
                    is_potential_bug = True
                    bug_signature = f"crash:{results[ERR_CPU_KEY] or results[ERR_GPU_KEY]}"
                elif results[ERR_CPU_KEY] and results[ERR_GPU_KEY]:
                    write_dir = join(self.output[oracle], "success")
                elif self.is_error_msg(results[ERR_CPU_KEY]) != self.is_error_msg(results[ERR_GPU_KEY]):
                    write_dir = join(self.output[oracle], "potential-bug")
                    is_potential_bug = True
                    bug_signature = f"error-diff:{results[ERR_CPU_KEY][:50] if results[ERR_CPU_KEY] else 'none'}|{results[ERR_GPU_KEY][:50] if results[ERR_GPU_KEY] else 'none'}"
                else:
                    write_dir = join(self.output[oracle], "success")
            elif self.is_crash_msg(error):
                write_dir = join(self.output[oracle], "potential-bug")
                is_potential_bug = True
                bug_signature = f"exec-crash:{error}"
            else:
                write_dir = join(self.output[oracle], "fail")
            
            # =========================================================
            # [FIX-1] 去重检查：跳过重复的 cuda bug
            # =========================================================
            if is_potential_bug and bug_signature:
                if self._is_duplicate_bug(bug_signature, "cuda"):
                    write_dir = None  # 跳过写入
            
            if write_dir:
                self.write_to_dir(write_dir, api.api, write_code)
            
        elif oracle == OracleType.PRECISION:
            code = "import torch\n"
            code += "import time\n"
            code += api.to_code(res=f"results[\"{TIME_LOW_KEY}\"]", low_precision=True)
            code += api.to_diff_code(oracle, res=f"results[\"{TIME_HIGH_KEY}\"]")

            write_code = "results = dict()\n" + code + "\nprint(results)\n"
            with open(join(self.directory, "temp.py"), "w") as f:
                f.write(write_code)

            results, error, kernels = self.run_code(code)
            if kernels: 
                captured_kernels.update(kernels)
            
            is_potential_bug = False
            bug_signature = None
            
            if error == None:
                if isinstance(results[TIME_LOW_KEY], float) and isinstance(results[TIME_HIGH_KEY], float):
                    if results[TIME_LOW_KEY] > self.time_bound * results[TIME_HIGH_KEY] and results[TIME_HIGH_KEY] > self.time_thresold:
                        write_dir = join(self.output[oracle], "potential-bug")
                        is_potential_bug = True
                        bug_signature = f"precision-slowdown:{results[TIME_LOW_KEY]:.2f}vs{results[TIME_HIGH_KEY]:.2f}"
                    else:
                        write_dir = join(self.output[oracle], "success")
                else:
                    write_dir = join(self.output[oracle], "fail")
            else:
                write_dir = join(self.output[oracle], "fail")
            
            # =========================================================
            # [FIX-1] 去重检查：跳过重复的 precision bug
            # =========================================================
            if is_potential_bug and bug_signature:
                if self._is_duplicate_bug(bug_signature, "precision"):
                    write_dir = join(self.output[oracle], "fail")  # 降级为 fail，不记录为 bug
            
            self.write_to_dir(write_dir, api.api, write_code)
        
        return captured_kernels

    @staticmethod
    def generate_code(api: TorchAPI, oracle: OracleType) -> str:
        if oracle == OracleType.CRASH:
            return api.to_code()
        elif oracle == OracleType.CUDA:
            code = api.to_code(res="cpu_res", use_try=True)
            code += api.to_diff_code(oracle, res="cuda_res", use_try=True)
            return code
        elif oracle == OracleType.PRECISION:
            code = api.to_code(res="low_res", low_precision=True)
            code += api.to_diff_code(oracle, res="high_res")
            return code
        else:
            assert(0)
    
    @staticmethod
    def run_code(code):
        results = dict()
        results[ERR_CPU_KEY] = None
        results[ERR_GPU_KEY] = None
        error = None
        kernels = set()

        try:
            is_cuda = torch.cuda.is_available()
            has_cuda_code = ".cuda" in code or ".to(" in code
            
            if is_cuda:
                with profile(activities=[ProfilerActivity.CUDA], record_shapes=False) as prof:
                    exec(code)
                
                all_events = list(prof.events())
                for event in all_events:
                    if "memcpy" not in event.name.lower():
                        kernels.add(event.name)
                
                if len(kernels) > 0:
                    print(f"\n\033[92m[Kernel-Probe] ✅ Captured {len(kernels)} kernels: {list(kernels)[:3]}...\033[0m")
                elif has_cuda_code:
                    print(f"\n\033[93m[Kernel-Probe] ⚠️ Code has '.cuda' but NO kernels. Events: {[e.name for e in all_events][:5]} \033[0m")
            else:
                exec(code)
                
        except Exception as e:
            error = str(e)
            
        return results, error, kernels
    
    @staticmethod
    def is_equal(x, y, diff_bound):
        def eq_float_tensor(x, y):
            return torch.allclose(x, y, atol=diff_bound, equal_nan=True)

        x_type = TorchArgument.get_type(x)
        y_type = TorchArgument.get_type(y)
        if x_type != y_type:
            if x_type == ArgType.TORCH_TENSOR and y_type in [ArgType.LIST, ArgType.TUPLE]:
                flag = False
                for temp in y:
                    flag = flag or TorchLibrary.is_equal(x, temp, diff_bound)
                return flag
            elif y_type == ArgType.TORCH_TENSOR and x_type in [ArgType.LIST, ArgType.TUPLE]:
                flag = False
                for temp in x:
                    flag = flag or TorchLibrary.is_equal(y, temp, diff_bound)
                return flag
            return False
        if x_type == ArgType.TORCH_TENSOR:
            x = x.cpu()
            y = y.cpu()
            if x.dtype != y.dtype or x.shape != y.shape:
                return False
            if x.is_sparse:
                x = x.to_dense()
            if y.is_sparse:
                y = y.to_dense()
            if x.is_complex():
                if not y.is_complex(): return False
                return eq_float_tensor(x.real, y.real) and eq_float_tensor(
                    x.imag, y.imag)
            if not x.dtype.is_floating_point:
                return torch.equal(x.cpu(), y.cpu())
            return eq_float_tensor(x, y)
        elif x_type == ArgType.FLOAT:
            return abs(x - y) < diff_bound
        elif x_type in [ArgType.LIST, ArgType.TUPLE]:
            if len(x) != len(y):
                return False
            for i in range(len(x)):
                if TorchLibrary.is_equal(x[i], y[i], diff_bound) == False:
                    return False
            return True
        else:
            return x == y
    
    @staticmethod
    def is_error_msg(error_msg):
        allowed_msgs = ["not implement", "not support"]

        if error_msg == None:
            return False
        for msg in allowed_msgs:
            if msg in error_msg:
                return False
        return True
    
    @staticmethod
    def is_crash_msg(error_msg):
        if error_msg == None:
            return False
        if "INTERNAL ASSERT" in error_msg:
            return True
        else:
            return False


def test():
    api_name = "torch.nn.Conv2d"
    api = TorchAPI(api_name)
    MyPytorch = TorchLibrary("torch-output")
    print(MyPytorch.generate_code(api, OracleType.CRASH))
    print(MyPytorch.generate_code(api, OracleType.CUDA))
    print(MyPytorch.generate_code(api, OracleType.PRECISION))
    MyPytorch.test_with_oracle(api, OracleType.CRASH)
    MyPytorch.test_with_oracle(api, OracleType.CUDA)
    MyPytorch.test_with_oracle(api, OracleType.PRECISION)