results = dict()
import torch
import time
arg_1 = 483
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.rand([0, np.int64(1024), 512], dtype=torch.bfloat16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
start = time.time()
results["time_low"] = arg_class(*arg_2)
results["time_low"] = time.time() - start
arg_2_0 = arg_2_0_tensor.clone().type(torch.bfloat16)
arg_2 = [arg_2_0,]
start = time.time()
results["time_high"] = arg_class(*arg_2)
results["time_high"] = time.time() - start

print(results)
