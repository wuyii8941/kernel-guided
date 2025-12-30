results = dict()
import torch
import time
arg_1_tensor = torch.rand([5, 2], dtype=torch.float16)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([5, 3], dtype=torch.float16)
arg_2 = arg_2_tensor.clone()
start = time.time()
results["time_low"] = torch.lstsq(arg_1,arg_2,)
results["time_low"] = time.time() - start
arg_1 = arg_1_tensor.clone().type(torch.float32)
arg_2 = arg_2_tensor.clone().type(torch.float32)
start = time.time()
results["time_high"] = torch.lstsq(arg_1,arg_2,)
results["time_high"] = time.time() - start

print(results)
