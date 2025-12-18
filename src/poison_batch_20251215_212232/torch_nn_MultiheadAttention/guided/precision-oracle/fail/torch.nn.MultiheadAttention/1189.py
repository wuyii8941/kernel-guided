results = dict()
import torch
import time
arg_1 = 512
arg_2 = 8
arg_3 = True
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([59, 0, 450, 31], dtype=torch.complex32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-32,1,[np.int64(1024), 0, 567, 1], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(0,4,[10, 52], dtype=torch.uint8)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
start = time.time()
results["time_low"] = arg_class(*arg_4)
results["time_low"] = time.time() - start
arg_4_0 = arg_4_0_tensor.clone().type(torch.complex64)
arg_4_1 = arg_4_1_tensor.clone().type(torch.int8)
arg_4_2 = arg_4_2_tensor.clone().type(torch.uint8)
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
start = time.time()
results["time_high"] = arg_class(*arg_4)
results["time_high"] = time.time() - start

print(results)
