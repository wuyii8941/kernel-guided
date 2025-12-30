results = dict()
import torch
import time
arg_1 = 16
arg_2 = "max"
arg_3 = 3
arg_4_0 = 2
arg_4_1 = 1
arg_4_2 = 2
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = 0
arg_6 = 0
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([8, 16, 128, 256], dtype=torch.float16)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
start = time.time()
results["time_low"] = arg_class(*arg_8)
results["time_low"] = time.time() - start
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_8_0 = arg_8_0_tensor.clone().type(torch.float32)
arg_8 = [arg_8_0,]
start = time.time()
results["time_high"] = arg_class(*arg_8)
results["time_high"] = time.time() - start

print(results)
