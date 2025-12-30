results = dict()
import torch
import time
arg_1 = 3
arg_2 = 9
arg_3_0 = 1
arg_3 = [arg_3_0,]
start = time.time()
results["time_low"] = torch.randint(arg_1,arg_2,size=arg_3,)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,]
start = time.time()
results["time_high"] = torch.randint(arg_1,arg_2,size=arg_3,)
results["time_high"] = time.time() - start

print(results)
