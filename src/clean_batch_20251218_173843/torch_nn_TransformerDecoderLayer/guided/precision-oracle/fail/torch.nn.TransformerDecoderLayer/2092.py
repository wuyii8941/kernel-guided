results = dict()
import torch
import time
arg_1 = 512
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-4,2,[20, 32, 527, 1], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-8,4,[10, 22, 555], dtype=torch.int8)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
start = time.time()
results["time_low"] = arg_class(*arg_3)
results["time_low"] = time.time() - start
arg_3_0 = arg_3_0_tensor.clone().type(torch.int64)
arg_3_1 = arg_3_1_tensor.clone().type(torch.int64)
arg_3 = [arg_3_0,arg_3_1,]
start = time.time()
results["time_high"] = arg_class(*arg_3)
results["time_high"] = time.time() - start

print(results)
