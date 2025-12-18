results = dict()
import torch
import time
arg_1 = 1536
arg_2 = 256
arg_3_tensor = torch.rand([40], dtype=torch.float16)
arg_3 = arg_3_tensor.clone()
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,bias=arg_3,kernel_size=arg_4,)
arg_5_0_tensor = torch.rand([16, 1536, 7, 7], dtype=torch.float16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
start = time.time()
results["time_low"] = arg_class(*arg_5)
results["time_low"] = time.time() - start
arg_3 = arg_3_tensor.clone().type(torch.float32)
arg_5_0 = arg_5_0_tensor.clone().type(torch.float32)
arg_5 = [arg_5_0,]
start = time.time()
results["time_high"] = arg_class(*arg_5)
results["time_high"] = time.time() - start

print(results)
