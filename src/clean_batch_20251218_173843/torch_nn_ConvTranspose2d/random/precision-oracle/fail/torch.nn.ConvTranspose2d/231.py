results = dict()
import torch
import time
arg_1 = 16
arg_2 = 16
arg_3 = -5
arg_4 = 2
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.randint(-1,64,[1, 31, 27, 50, 1], dtype=torch.int8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_6_0 = arg_6_0_tensor.clone().type(torch.int8)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
