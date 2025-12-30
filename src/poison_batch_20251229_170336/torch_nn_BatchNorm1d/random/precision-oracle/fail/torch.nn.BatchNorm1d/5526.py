results = dict()
import torch
import time
arg_1 = 32
arg_class = torch.nn.BatchNorm1d(arg_1,)
arg_2_0_tensor = torch.rand([64, 12544], dtype=torch.complex32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
start = time.time()
results["time_low"] = arg_class(*arg_2)
results["time_low"] = time.time() - start
arg_2_0 = arg_2_0_tensor.clone().type(torch.complex64)
arg_2 = [arg_2_0,]
start = time.time()
results["time_high"] = arg_class(*arg_2)
results["time_high"] = time.time() - start

print(results)
