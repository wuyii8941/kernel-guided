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
    
    def test_with_oracle(self, api: TorchAPI, oracle: OracleType):
        captured_kernels = set()
        
        if oracle == OracleType.CRASH:
            # We need call another process to catch the crash error
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
            if error == None:
                # first check the correctness
                if results[ERR_CPU_KEY] == None and results[ERR_GPU_KEY] == None:
                    try:
                        is_equal = self.is_equal(results[RES_CPU_KEY], results[RES_GPU_KEY], self.diff_bound)
                    except Exception:
                        write_dir = join(self.output[oracle], "compare-bug")
                    else:
                        if is_equal:
                            write_dir = join(self.output[oracle], "success")
                        else:
                            write_dir = join(self.output[oracle], "potential-bug")
                elif self.is_crash_msg(results[ERR_CPU_KEY]) or self.is_crash_msg(results[ERR_GPU_KEY]):
                    write_dir = join(self.output[oracle], "potential-bug")
                elif results[ERR_CPU_KEY] and results[ERR_GPU_KEY]:
                    write_dir = join(self.output[oracle], "success")
                    pass
                elif self.is_error_msg(results[ERR_CPU_KEY]) != self.is_error_msg(results[ERR_GPU_KEY]):
                    write_dir = join(self.output[oracle], "potential-bug")
                else:
                    write_dir = join(self.output[oracle], "success")
            elif self.is_crash_msg(error):
                write_dir = join(self.output[oracle], "potential-bug")
            else:
                write_dir = join(self.output[oracle], "fail")
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
            
            if error == None:
                if isinstance(results.get(TIME_LOW_KEY), float) and isinstance(results.get(TIME_HIGH_KEY), float):
                    if results[TIME_LOW_KEY] > self.time_bound * results[TIME_HIGH_KEY] and results[TIME_HIGH_KEY] > self.time_thresold:
                        write_dir = join(self.output[oracle], "potential-bug")
                    else:
                        write_dir = join(self.output[oracle], "success")
                else:
                    write_dir = join(self.output[oracle], "fail")
            else:
                write_dir = join(self.output[oracle], "fail")
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

        # 🔧 修复：创建共享命名空间，让 exec 内部可以访问和修改 results
        exec_namespace = {'results': results, 'torch': torch}

        try:
            is_cuda = torch.cuda.is_available()
            has_cuda_code = ".cuda" in code or ".to(" in code
            
            if is_cuda:
                with profile(activities=[ProfilerActivity.CUDA], record_shapes=False) as prof:
                    exec(code, exec_namespace)
                
                # 解析 Kernel
                all_events = list(prof.events())
                for event in all_events:
                    if "memcpy" not in event.name.lower():
                        kernels.add(event.name)
                
                if len(kernels) > 0:
                    print(f"\n\033[92m[Kernel-Probe] ✅ Captured {len(kernels)} kernels: {list(kernels)[:3]}...\033[0m")
                elif has_cuda_code:
                    print(f"\n\033[93m[Kernel-Probe] ⚠️ Code has '.cuda' but NO kernels. Events: {[e.name for e in all_events][:5]} \033[0m")
            else:
                exec(code, exec_namespace)
                
        except Exception as e:
            error = str(e)
        
        # 🔧 修复：从共享命名空间获取更新后的 results
        results = exec_namespace.get('results', results)
            
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