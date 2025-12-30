import torch
arg_1_0 = 2
arg_1_1 = 3
arg_1 = [arg_1_0,arg_1_1,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(-32,128,[77, 1, 24, 24], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
