results = dict()
import torch
import time
arg_1 = "max"
arg_2 = 0.0
arg_class = torch.nn.BatchNorm1d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.rand([999, 100], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
start = time.time()
results["time_low"] = arg_class(*arg_3)
results["time_low"] = time.time() - start
arg_3_0 = arg_3_0_tensor.clone().type(torch.bfloat16)
arg_3 = [arg_3_0,]
start = time.time()
results["time_high"] = arg_class(*arg_3)
results["time_high"] = time.time() - start

print(results)
