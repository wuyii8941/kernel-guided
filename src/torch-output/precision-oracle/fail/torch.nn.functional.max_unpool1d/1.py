results = dict()
import torch
import time
arg_1_tensor = torch.rand([1, 1, 4], dtype=torch.float16)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.randint(-8,2,[1, 1, 4], dtype=torch.int8)
arg_2 = arg_2_tensor.clone()
arg_3_0 = 37
arg_3 = [arg_3_0,]
arg_4_0 = -7
arg_4 = [arg_4_0,]
arg_5_0 = 0
arg_5 = [arg_5_0,]
arg_6_0 = 1
arg_6_1 = 1
arg_6_2 = 9
arg_6 = [arg_6_0,arg_6_1,arg_6_2,]
start = time.time()
results["time_low"] = torch.nn.functional.max_unpool1d(arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
results["time_low"] = time.time() - start
arg_1 = arg_1_tensor.clone().type(torch.float32)
arg_2 = arg_2_tensor.clone().type(torch.int64)
arg_3 = [arg_3_0,]
arg_4 = [arg_4_0,]
arg_5 = [arg_5_0,]
arg_6 = [arg_6_0,arg_6_1,arg_6_2,]
start = time.time()
results["time_high"] = torch.nn.functional.max_unpool1d(arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
results["time_high"] = time.time() - start

print(results)
