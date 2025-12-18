results = dict()
import torch
import time
arg_1 = 1
arg_2 = 1991
arg_3 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,)
arg_4_0_tensor = torch.rand([80, 2048, 6, 6], dtype=torch.float16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.float32)
arg_4 = [arg_4_0,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
