results = dict()
import torch
import time
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.rand([6, 2], dtype=torch.bfloat16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(0,2,[5, 2], dtype=torch.bool)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
start = time.time()
results["time_low"] = arg_class(*arg_1)
results["time_low"] = time.time() - start
arg_1_0 = arg_1_0_tensor.clone().type(torch.bfloat16)
arg_1_1 = arg_1_1_tensor.clone().type(torch.bool)
arg_1 = [arg_1_0,arg_1_1,]
start = time.time()
results["time_high"] = arg_class(*arg_1)
results["time_high"] = time.time() - start

print(results)
