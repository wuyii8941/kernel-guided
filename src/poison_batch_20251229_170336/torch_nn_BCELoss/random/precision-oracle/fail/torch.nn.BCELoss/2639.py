results = dict()
import torch
import time
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-128,8,[0], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16,8,[3, 1], dtype=torch.int8)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
start = time.time()
results["time_low"] = arg_class(*arg_1)
results["time_low"] = time.time() - start
arg_1_0 = arg_1_0_tensor.clone().type(torch.int32)
arg_1_1 = arg_1_1_tensor.clone().type(torch.int32)
arg_1 = [arg_1_0,arg_1_1,]
start = time.time()
results["time_high"] = arg_class(*arg_1)
results["time_high"] = time.time() - start

print(results)
