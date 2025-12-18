results = dict()
import torch
import time
arg_1 = 512
arg_2 = -24
arg_3_0 = 3
arg_3_1 = 5
arg_3_2 = 2
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.rand([80, 512, 16, 16], dtype=torch.float16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
start = time.time()
results["time_low"] = arg_class(*arg_5)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_5_0 = arg_5_0_tensor.clone().type(torch.float32)
arg_5 = [arg_5_0,]
start = time.time()
results["time_high"] = arg_class(*arg_5)
results["time_high"] = time.time() - start

print(results)
