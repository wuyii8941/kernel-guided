results = dict()
import torch
import time
arg_1 = 16
arg_2 = -17.0
arg_3_0 = 63.0
arg_3_1 = False
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = -12
arg_5_0 = 0
arg_5_1 = 1
arg_5 = [arg_5_0,arg_5_1,]
arg_6 = True
arg_7_0 = 1
arg_7_1 = 1
arg_7 = [arg_7_0,arg_7_1,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,bias=arg_6,dilation=arg_7,)
arg_8_0_tensor = torch.rand([8, 16, 128, 256], dtype=torch.float16)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
start = time.time()
results["time_low"] = arg_class(*arg_8)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,]
arg_5 = [arg_5_0,arg_5_1,]
arg_7 = [arg_7_0,arg_7_1,]
arg_8_0 = arg_8_0_tensor.clone().type(torch.float32)
arg_8 = [arg_8_0,]
start = time.time()
results["time_high"] = arg_class(*arg_8)
results["time_high"] = time.time() - start

print(results)
