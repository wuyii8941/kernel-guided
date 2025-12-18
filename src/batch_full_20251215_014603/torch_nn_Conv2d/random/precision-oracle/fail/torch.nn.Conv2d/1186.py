results = dict()
import torch
import time
arg_1 = 16
arg_2 = 33
arg_3_0 = -58
arg_3_1 = 34
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = 63
arg_4_1 = -35
arg_4 = [arg_4_0,arg_4_1,]
arg_5_0 = -38
arg_5_1 = -26
arg_5 = [arg_5_0,arg_5_1,]
arg_6_0 = "max"
arg_6_1 = "max"
arg_6 = [arg_6_0,arg_6_1,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,dilation=arg_6,)
arg_7_0_tensor = torch.rand([20, 16, 50, 100], dtype=torch.float16)
arg_7_0 = arg_7_0_tensor.clone()
arg_7 = [arg_7_0,]
start = time.time()
results["time_low"] = arg_class(*arg_7)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = [arg_4_0,arg_4_1,]
arg_5 = [arg_5_0,arg_5_1,]
arg_6 = [arg_6_0,arg_6_1,]
arg_7_0 = arg_7_0_tensor.clone().type(torch.float32)
arg_7 = [arg_7_0,]
start = time.time()
results["time_high"] = arg_class(*arg_7)
results["time_high"] = time.time() - start

print(results)
