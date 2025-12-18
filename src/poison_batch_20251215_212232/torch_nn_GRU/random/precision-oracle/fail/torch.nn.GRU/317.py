results = dict()
import torch
import time
arg_1 = -inf
arg_2 = 128
arg_3 = "max"
arg_4 = True
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([100, 1, 1], dtype=torch.float16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.rand([1, 100, 128], dtype=torch.float16)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
start = time.time()
results["time_low"] = arg_class(*arg_5)
results["time_low"] = time.time() - start
arg_5_0 = arg_5_0_tensor.clone().type(torch.float32)
arg_5_1 = arg_5_1_tensor.clone().type(torch.float32)
arg_5 = [arg_5_0,arg_5_1,]
start = time.time()
results["time_high"] = arg_class(*arg_5)
results["time_high"] = time.time() - start

print(results)
