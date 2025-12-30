results = dict()
import torch
import time
arg_1_0 = 1
arg_1_1 = 30
arg_1 = [arg_1_0,arg_1_1,]
arg_2_0 = -28
arg_2_1 = -16
arg_2 = [arg_2_0,arg_2_1,]
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-64,8,[1, 296, 8, 74], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
start = time.time()
results["time_low"] = arg_class(*arg_3)
results["time_low"] = time.time() - start
arg_1 = [arg_1_0,arg_1_1,]
arg_2 = [arg_2_0,arg_2_1,]
arg_3_0 = arg_3_0_tensor.clone().type(torch.int8)
arg_3 = [arg_3_0,]
start = time.time()
results["time_high"] = arg_class(*arg_3)
results["time_high"] = time.time() - start

print(results)
