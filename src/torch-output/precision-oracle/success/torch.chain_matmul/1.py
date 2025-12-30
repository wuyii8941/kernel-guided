results = dict()
import torch
import time
arg_1_tensor = torch.rand([6, 2], dtype=torch.float16)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([2, 4], dtype=torch.float16)
arg_2 = arg_2_tensor.clone()
arg_3_tensor = torch.rand([4, 8], dtype=torch.float16)
arg_3 = arg_3_tensor.clone()
arg_4_tensor = torch.rand([8, 10], dtype=torch.float16)
arg_4 = arg_4_tensor.clone()
start = time.time()
results["time_low"] = torch.chain_matmul(arg_1,arg_2,arg_3,arg_4,)
results["time_low"] = time.time() - start
arg_1 = arg_1_tensor.clone().type(torch.float64)
arg_2 = arg_2_tensor.clone().type(torch.float64)
arg_3 = arg_3_tensor.clone().type(torch.float64)
arg_4 = arg_4_tensor.clone().type(torch.float64)
start = time.time()
results["time_high"] = torch.chain_matmul(arg_1,arg_2,arg_3,arg_4,)
results["time_high"] = time.time() - start

print(results)
