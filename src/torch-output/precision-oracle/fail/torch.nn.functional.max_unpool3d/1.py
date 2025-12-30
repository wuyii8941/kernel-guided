results = dict()
import torch
import time
arg_1_tensor = torch.rand([20, 16, 25, 16, 7], dtype=torch.float16)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.randint(-64,8,[20, 16, 25, 16, 7], dtype=torch.int8)
arg_2 = arg_2_tensor.clone()
arg_3_0 = 3
arg_3_1 = 3
arg_3_2 = 3
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4_0 = 2
arg_4_1 = 2
arg_4_2 = 2
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = 0
arg_5_1 = 0
arg_5_2 = 0
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_6 = None
start = time.time()
results["time_low"] = torch.nn.functional.max_unpool3d(arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
results["time_low"] = time.time() - start
arg_1 = arg_1_tensor.clone().type(torch.float32)
arg_2 = arg_2_tensor.clone().type(torch.int64)
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
start = time.time()
results["time_high"] = torch.nn.functional.max_unpool3d(arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
results["time_high"] = time.time() - start

print(results)
