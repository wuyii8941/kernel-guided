results = dict()
import torch
import time
arg_1 = 20
arg_2 = 69
arg_3 = 40
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([173, 20], dtype=torch.float16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([128, 0], dtype=torch.float16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.float32)
arg_4_1 = arg_4_1_tensor.clone().type(torch.float32)
arg_4 = [arg_4_0,arg_4_1,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
