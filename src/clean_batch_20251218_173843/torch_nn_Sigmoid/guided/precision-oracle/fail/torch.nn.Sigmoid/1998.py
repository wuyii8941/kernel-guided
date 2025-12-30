results = dict()
import torch
import time
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.rand([48, 1024, 4, 4], dtype=torch.float16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
start = time.time()
results["time_low"] = arg_class(*arg_1)
results["time_low"] = time.time() - start
arg_1_0 = arg_1_0_tensor.clone().type(torch.float32)
arg_1 = [arg_1_0,]
start = time.time()
results["time_high"] = arg_class(*arg_1)
results["time_high"] = time.time() - start

print(results)
