results = dict()
import torch
import time
arg_1_tensor = torch.rand([16, 1024, 1, 1], dtype=torch.float16)
arg_1 = arg_1_tensor.clone()
arg_2 = 21.2
arg_3 = "max"
start = time.time()
results["time_low"] = torch.nn.functional.leaky_relu(arg_1,arg_2,arg_3,)
results["time_low"] = time.time() - start
arg_1 = arg_1_tensor.clone().type(torch.float32)
start = time.time()
results["time_high"] = torch.nn.functional.leaky_relu(arg_1,arg_2,arg_3,)
results["time_high"] = time.time() - start

print(results)
