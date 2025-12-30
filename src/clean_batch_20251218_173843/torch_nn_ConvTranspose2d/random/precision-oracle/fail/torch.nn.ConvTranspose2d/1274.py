results = dict()
import torch
import time
arg_1 = 128
arg_2 = 16
arg_3 = 3
arg_4 = 2
arg_5_0 = 0
arg_5_1 = 4
arg_5_2 = 2
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([1, 16, 6, 6], dtype=torch.float16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_6_0 = arg_6_0_tensor.clone().type(torch.float32)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
