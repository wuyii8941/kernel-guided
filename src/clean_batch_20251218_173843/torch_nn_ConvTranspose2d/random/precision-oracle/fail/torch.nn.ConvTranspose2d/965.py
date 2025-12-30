results = dict()
import torch
import time
arg_1 = 64
arg_2 = 3
arg_3 = -16
arg_4 = 2
arg_5 = 57
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([158, 64, 14, 14], dtype=torch.float16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_6_0 = arg_6_0_tensor.clone().type(torch.float32)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
