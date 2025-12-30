results = dict()
import torch
import time
arg_1 = 3
arg_2_0 = 2
arg_2_1 = 2
arg_2_2 = 2
arg_2 = [arg_2_0,arg_2_1,arg_2_2,]
arg_3 = 1
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([128, 192, 16, 16], dtype=torch.float16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_2 = [arg_2_0,arg_2_1,arg_2_2,]
arg_4_0 = arg_4_0_tensor.clone().type(torch.float32)
arg_4 = [arg_4_0,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
