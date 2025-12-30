import torch
arg_1 = 1
arg_2 = "max"
arg_class = torch.nn.GroupNorm(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-512,8192,[20, 6, 10, 5], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
