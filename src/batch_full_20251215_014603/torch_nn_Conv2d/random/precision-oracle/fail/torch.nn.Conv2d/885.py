results = dict()
import torch
import time
arg_1 = 32
arg_2 = -13
arg_3 = 9
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,)
arg_5_0_tensor = torch.randint(-1,4,[0, 0, 1088, 1088], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
start = time.time()
results["time_low"] = arg_class(*arg_5)
results["time_low"] = time.time() - start
arg_5_0 = arg_5_0_tensor.clone().type(torch.int8)
arg_5 = [arg_5_0,]
start = time.time()
results["time_high"] = arg_class(*arg_5)
results["time_high"] = time.time() - start

print(results)
