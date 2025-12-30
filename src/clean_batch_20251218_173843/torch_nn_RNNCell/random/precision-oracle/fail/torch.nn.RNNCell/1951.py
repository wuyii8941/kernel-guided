results = dict()
import torch
import time
arg_1 = 31
arg_2 = 20
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([3, 10], dtype=torch.float16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([3, 20], dtype=torch.float16)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
start = time.time()
results["time_low"] = arg_class(*arg_3)
results["time_low"] = time.time() - start
arg_3_0 = arg_3_0_tensor.clone().type(torch.float32)
arg_3_1 = arg_3_1_tensor.clone().type(torch.float32)
arg_3 = [arg_3_0,arg_3_1,]
start = time.time()
results["time_high"] = arg_class(*arg_3)
results["time_high"] = time.time() - start

print(results)
