results = dict()
import torch
import time
arg_1 = 1
arg_2 = 128
arg_3 = 1
arg_4 = -28
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-64,32,[143, 1, np.int64(1024)], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.randint(0,8,[1, 0, 180, np.int64(16)], dtype=torch.uint8)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
start = time.time()
results["time_low"] = arg_class(*arg_5)
results["time_low"] = time.time() - start
arg_5_0 = arg_5_0_tensor.clone().type(torch.int16)
arg_5_1 = arg_5_1_tensor.clone().type(torch.uint8)
arg_5 = [arg_5_0,arg_5_1,]
start = time.time()
results["time_high"] = arg_class(*arg_5)
results["time_high"] = time.time() - start

print(results)
