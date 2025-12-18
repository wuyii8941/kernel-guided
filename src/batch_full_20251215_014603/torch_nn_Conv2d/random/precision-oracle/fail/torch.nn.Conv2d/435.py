results = dict()
import torch
import time
arg_1 = 512
arg_2 = 2048
arg_3 = 3
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([80, 551, 31, 16], dtype=torch.float16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.float64)
arg_4 = [arg_4_0,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
