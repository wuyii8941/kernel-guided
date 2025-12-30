results = dict()
import torch
import time
arg_1 = 512
arg_2 = 8
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-1,64,[20, 0, 488], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([20, 32, 512], dtype=torch.float16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-2,8,[17, 32, 512, 1], dtype=torch.int8)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.int64)
arg_4_1 = arg_4_1_tensor.clone().type(torch.float32)
arg_4_2 = arg_4_2_tensor.clone().type(torch.int32)
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
