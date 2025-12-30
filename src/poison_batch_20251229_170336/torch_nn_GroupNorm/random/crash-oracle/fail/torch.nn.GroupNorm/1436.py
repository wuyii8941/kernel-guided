import torch
arg_1 = nan
arg_2 = 10
arg_class = torch.nn.GroupNorm(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-4096,128,[20, 5, 10], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
