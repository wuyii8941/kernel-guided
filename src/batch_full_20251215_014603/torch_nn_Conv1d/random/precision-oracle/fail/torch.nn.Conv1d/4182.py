results = dict()
import torch
import time
arg_1 = 16
arg_2 = 33
arg_3_0 = 41.0
arg_3_1 = 1.0
arg_3_2 = "max"
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = -60
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-4,2,[58, 9, 55, 1], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
start = time.time()
results["time_low"] = arg_class(*arg_5)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_5_0 = arg_5_0_tensor.clone().type(torch.int64)
arg_5 = [arg_5_0,]
start = time.time()
results["time_high"] = arg_class(*arg_5)
results["time_high"] = time.time() - start

print(results)
