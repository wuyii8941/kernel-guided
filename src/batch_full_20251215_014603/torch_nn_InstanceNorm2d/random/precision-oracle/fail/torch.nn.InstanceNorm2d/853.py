results = dict()
import torch
import time
arg_1 = 39
arg_class = torch.nn.InstanceNorm2d(arg_1,)
arg_2_0_tensor = torch.rand([1, 1, 0, 35, 1], dtype=torch.float16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
start = time.time()
results["time_low"] = arg_class(*arg_2)
results["time_low"] = time.time() - start
arg_2_0 = arg_2_0_tensor.clone().type(torch.float64)
arg_2 = [arg_2_0,]
start = time.time()
results["time_high"] = arg_class(*arg_2)
results["time_high"] = time.time() - start

print(results)
