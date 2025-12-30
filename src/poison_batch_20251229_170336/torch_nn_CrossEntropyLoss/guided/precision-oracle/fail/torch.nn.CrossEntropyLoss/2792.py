results = dict()
import torch
import time
arg_class = torch.nn.CrossEntropyLoss()
arg_1_0_tensor = torch.rand([80, 99], dtype=torch.complex32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-1,2,[0], dtype=torch.int8)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
start = time.time()
results["time_low"] = arg_class(*arg_1)
results["time_low"] = time.time() - start
arg_1_0 = arg_1_0_tensor.clone().type(torch.complex128)
arg_1_1 = arg_1_1_tensor.clone().type(torch.int64)
arg_1 = [arg_1_0,arg_1_1,]
start = time.time()
results["time_high"] = arg_class(*arg_1)
results["time_high"] = time.time() - start

print(results)
