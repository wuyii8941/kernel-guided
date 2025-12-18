results = dict()
import torch
import time
arg_1 = 123
arg_2 = 16
arg_3 = 9
arg_4 = 63.0
arg_5 = 1
arg_6 = False
arg_class = torch.nn.Conv2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,bias=arg_6,)
arg_7_0_tensor = torch.rand([26, 128, 144, 144], dtype=torch.float16)
arg_7_0 = arg_7_0_tensor.clone()
arg_7 = [arg_7_0,]
start = time.time()
results["time_low"] = arg_class(*arg_7)
results["time_low"] = time.time() - start
arg_7_0 = arg_7_0_tensor.clone().type(torch.float32)
arg_7 = [arg_7_0,]
start = time.time()
results["time_high"] = arg_class(*arg_7)
results["time_high"] = time.time() - start

print(results)
