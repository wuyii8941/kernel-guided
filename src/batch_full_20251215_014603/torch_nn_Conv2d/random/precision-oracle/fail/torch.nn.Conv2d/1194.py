results = dict()
import torch
import time
arg_1 = 512
arg_2 = False
arg_3 = 1
arg_4 = 1
arg_5 = 0
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([np.int64(1), 64, 28], dtype=torch.complex32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
start = time.time()
results["time_low"] = arg_class(*arg_6)
results["time_low"] = time.time() - start
arg_6_0 = arg_6_0_tensor.clone().type(torch.complex64)
arg_6 = [arg_6_0,]
start = time.time()
results["time_high"] = arg_class(*arg_6)
results["time_high"] = time.time() - start

print(results)
