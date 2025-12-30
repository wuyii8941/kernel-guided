import torch
arg_1_0 = -1024
arg_1_1 = -7
arg_1 = [arg_1_0,arg_1_1,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(0,2,[32, 5, 24], dtype=torch.bool)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
