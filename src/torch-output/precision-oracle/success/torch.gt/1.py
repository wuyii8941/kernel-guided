results = dict()
import torch
import time
arg_1_tensor = torch.randint(-4,128,[2, 2], dtype=torch.int8)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.randint(-32,4,[2, 2], dtype=torch.int8)
arg_2 = arg_2_tensor.clone()
start = time.time()
results["time_low"] = torch.gt(arg_1,arg_2,)
results["time_low"] = time.time() - start
arg_1 = arg_1_tensor.clone().type(torch.int64)
arg_2 = arg_2_tensor.clone().type(torch.int64)
start = time.time()
results["time_high"] = torch.gt(arg_1,arg_2,)
results["time_high"] = time.time() - start

print(results)
