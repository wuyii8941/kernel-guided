results = dict()
import torch
import time
arg_1 = 16
arg_2 = 204
arg_3_0 = 3
arg_3_1 = 3
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 2
arg_5_0 = -1
arg_5_1 = 0
arg_5_2 = -1
arg_5_3 = 0
arg_5 = [arg_5_0,arg_5_1,arg_5_2,arg_5_3,]
arg_6 = 0
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([1, 256, 28, 28], dtype=torch.float16)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
start = time.time()
results["time_low"] = arg_class(*arg_8)
results["time_low"] = time.time() - start
arg_3 = [arg_3_0,arg_3_1,]
arg_5 = [arg_5_0,arg_5_1,arg_5_2,arg_5_3,]
arg_8_0 = arg_8_0_tensor.clone().type(torch.float32)
arg_8 = [arg_8_0,]
start = time.time()
results["time_high"] = arg_class(*arg_8)
results["time_high"] = time.time() - start

print(results)
