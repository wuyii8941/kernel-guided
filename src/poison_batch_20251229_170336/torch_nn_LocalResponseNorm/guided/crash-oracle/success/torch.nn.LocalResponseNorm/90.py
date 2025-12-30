import torch
arg_1_0 = 2
arg_1_1 = 3
arg_1_2 = 12
arg_1_3 = 13
arg_1 = [arg_1_0,arg_1_1,arg_1_2,arg_1_3,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(-16384,8192,[39, 0, 21, 24], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
