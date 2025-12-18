results = dict()
import torch
import time
arg_1 = 545
arg_2 = 2048
arg_3 = 1
arg_4_tensor = torch.rand([32], dtype=torch.float16)
arg_4 = arg_4_tensor.clone()
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.randint(-1,16,[51, 512, 8, 11], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
start = time.time()
results["time_low"] = arg_class(*arg_5)
results["time_low"] = time.time() - start
arg_4 = arg_4_tensor.clone().type(torch.float32)
arg_5_0 = arg_5_0_tensor.clone().type(torch.int8)
arg_5 = [arg_5_0,]
start = time.time()
results["time_high"] = arg_class(*arg_5)
results["time_high"] = time.time() - start

print(results)
