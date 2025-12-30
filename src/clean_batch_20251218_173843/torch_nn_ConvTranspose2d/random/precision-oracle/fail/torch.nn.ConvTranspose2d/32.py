results = dict()
import torch
import time
arg_1 = 16
arg_2 = 2
arg_3 = 2
arg_4 = 1024
arg_5 = 0
arg_6_0 = 0
arg_6_1 = 0
arg_6_2 = 0
arg_6 = [arg_6_0,arg_6_1,arg_6_2,]
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.randint(-16,2,[8, 0, 186, 1, 1], dtype=torch.int8)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
start = time.time()
results["time_low"] = arg_class(*arg_8)
results["time_low"] = time.time() - start
arg_6 = [arg_6_0,arg_6_1,arg_6_2,]
arg_8_0 = arg_8_0_tensor.clone().type(torch.int64)
arg_8 = [arg_8_0,]
start = time.time()
results["time_high"] = arg_class(*arg_8)
results["time_high"] = time.time() - start

print(results)
