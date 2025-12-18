results = dict()
import torch
import time
arg_1 = 128
arg_2 = 1024.0
arg_3 = 3
arg_4 = 1
arg_5_tensor = torch.rand([64], dtype=torch.float16)
arg_5 = arg_5_tensor.clone()
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.rand([80, 128, 4, 4], dtype=torch.float16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_5 = arg_5_tensor.clone().type(torch.float32)
arg_6_0 = arg_6_0_tensor.clone().type(torch.float32)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
