results = dict()
import torch
import time
arg_1 = 44.0
arg_2 = 20
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-4,128,[5, 8, 10], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([29, 0, 20], dtype=torch.complex32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.int8)
arg_4_1 = arg_4_1_tensor.clone().type(torch.complex128)
arg_4 = [arg_4_0,arg_4_1,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
