results = dict()
import torch
import time
arg_1 = 35
arg_2 = 1
arg_3_0 = 1
arg_3_1 = 1
arg_3 = [arg_3_0,arg_3_1,]
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(0,16,[136, 480, 16, 54], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = arg_4_0_tensor.clone().type(torch.uint8)
arg_4 = [arg_4_0,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
