results = dict()
import torch
import time
arg_1 = 16
arg_2 = 33
arg_3_0 = 49
arg_3_1 = 61
arg_3_2 = 63
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4_0 = 2
arg_4_1 = 1
arg_4_2 = 1
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = 13
arg_5_1 = 42
arg_5_2 = 2
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.randint(0,2,[20, 75, 10, np.int64(16), 100], dtype=torch.uint8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_6_0 = arg_6_0_tensor.clone().type(torch.uint8)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
