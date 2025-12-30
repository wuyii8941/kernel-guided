results = dict()
import torch
import time
arg_1 = 3
arg_2 = 1
arg_3 = 41
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(0,64,[1, 64, 112, 112], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.uint8)
arg_4 = [arg_4_0,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
