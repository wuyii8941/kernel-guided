results = dict()
import torch
import time
arg_1 = False
arg_2 = 2
arg_3 = 0
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(0,2,[16, 480, 16, 0], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.bool)
arg_4 = [arg_4_0,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
