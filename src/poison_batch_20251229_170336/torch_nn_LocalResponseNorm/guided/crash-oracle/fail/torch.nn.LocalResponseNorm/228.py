import torch
arg_1_0 = 16
arg_1_1 = 16
arg_1 = [arg_1_0,arg_1_1,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(-2,64,[32, 16, 22, 24], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
