results = dict()
import torch
import time
arg_1 = 2
arg_2 = -44
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,)
arg_3_0_tensor = torch.rand([80, 512, 2, 2], dtype=torch.float16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
start = time.time()
results["time_low"] = arg_class(*arg_3)
results["time_low"] = time.time() - start
arg_3_0 = arg_3_0_tensor.clone().type(torch.float32)
arg_3 = [arg_3_0,]
start = time.time()
results["time_high"] = arg_class(*arg_3)
results["time_high"] = time.time() - start

print(results)
