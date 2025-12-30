results = dict()
import torch
import time
arg_1 = 1029
arg_2 = -96.0
arg_3_tensor = torch.rand([768], dtype=torch.float16)
arg_3 = arg_3_tensor.clone()
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.rand([5, 1, 1024], dtype=torch.float16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_3 = arg_3_tensor.clone().type(torch.float32)
arg_4_0 = arg_4_0_tensor.clone().type(torch.float32)
arg_4 = [arg_4_0,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
