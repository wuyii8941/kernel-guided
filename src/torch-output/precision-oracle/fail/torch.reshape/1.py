results = dict()
import torch
import time
arg_1_tensor = torch.randint(-8,64,[2, 2], dtype=torch.int8)
arg_1 = arg_1_tensor.clone()
arg_2_0 = -56
arg_2 = [arg_2_0,]
start = time.time()
results["time_low"] = torch.reshape(arg_1,arg_2,)
results["time_low"] = time.time() - start
arg_1 = arg_1_tensor.clone().type(torch.int64)
arg_2 = [arg_2_0,]
start = time.time()
results["time_high"] = torch.reshape(arg_1,arg_2,)
results["time_high"] = time.time() - start

print(results)
