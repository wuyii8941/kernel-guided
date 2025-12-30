import torch
arg_1_0 = 2
arg_1_1 = 1
arg_1_2 = 1
arg_1_3 = 2
arg_1 = [arg_1_0,arg_1_1,arg_1_2,arg_1_3,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([16, 5, 7, 7, 7, 7, 1], dtype=torch.bfloat16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
