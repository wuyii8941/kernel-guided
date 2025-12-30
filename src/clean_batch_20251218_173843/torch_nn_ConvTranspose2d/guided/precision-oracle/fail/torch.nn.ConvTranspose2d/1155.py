results = dict()
import torch
import time
arg_1 = -1
arg_2 = 11
arg_3_0 = 3
arg_3_1 = 5
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = 44
arg_4_1 = 64
arg_4 = [arg_4_0,arg_4_1,]
arg_5 = -54
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([20, 16, 50, 100], dtype=torch.float16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = [arg_4_0,arg_4_1,]
arg_6_0 = arg_6_0_tensor.clone().type(torch.float32)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
