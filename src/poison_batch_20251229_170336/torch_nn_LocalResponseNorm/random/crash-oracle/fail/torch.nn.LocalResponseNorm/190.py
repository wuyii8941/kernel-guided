import torch
arg_1_0 = 2
arg_1_1 = 2
arg_1 = [arg_1_0,arg_1_1,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([-1, 5, 7, 0, 13, 7], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
