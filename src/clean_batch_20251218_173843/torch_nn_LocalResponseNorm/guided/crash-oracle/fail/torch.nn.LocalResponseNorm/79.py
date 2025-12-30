import torch
arg_1 = 72
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(-8192,128,[32, 30, 24], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
