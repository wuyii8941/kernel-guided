results = dict()
import torch
import time
arg_1 = 16
arg_2 = -43.0
arg_3_0 = "max"
arg_3_1 = 964.0
arg_3_2 = "max"
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4_0 = -21
arg_4_1 = -11
arg_4_2 = 62
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = -52
arg_5_1 = -23
arg_5_2 = -48
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([20, 16, 10, 50, 100], dtype=torch.float16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_6_0 = arg_6_0_tensor.clone().type(torch.float32)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
