import torch
arg_1_0 = 20
arg_1_1 = 16
arg_1_2 = 50
arg_1_3 = 44
arg_1_4 = 31
arg_1 = [arg_1_0,arg_1_1,arg_1_2,arg_1_3,arg_1_4,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([32, 16, 24, 27], dtype=torch.float16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
