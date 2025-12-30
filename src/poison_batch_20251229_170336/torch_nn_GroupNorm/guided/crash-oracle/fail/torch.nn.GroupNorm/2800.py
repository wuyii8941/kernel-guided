import torch
arg_1 = -5.953987674061728
arg_2 = 11
arg_class = torch.nn.GroupNorm(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-64,32,[20, 6, 10, 10], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
