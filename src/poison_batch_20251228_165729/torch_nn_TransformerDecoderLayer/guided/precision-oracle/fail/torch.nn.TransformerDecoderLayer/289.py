results = dict()
import torch
import time
arg_1 = 515
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,).cuda()
arg_3_0_tensor = torch.rand([1, 35, 512], dtype=torch.float16)
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_tensor = torch.rand([2, 11, 512], dtype=torch.float16)
arg_3_1 = arg_3_1_tensor.clone().cuda()
arg_3 = [arg_3_0,arg_3_1,]
start = time.time()
results["time_low"] = arg_class(*arg_3)
results["time_low"] = time.time() - start
arg_3_0 = arg_3_0_tensor.clone().type(torch.float32)
arg_3_1 = arg_3_1_tensor.clone().type(torch.float32)
arg_3 = [arg_3_0,arg_3_1,]
start = time.time()
results["time_high"] = arg_class(*arg_3)
results["time_high"] = time.time() - start

print(results)
