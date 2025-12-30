import torch
arg_1_0 = 4
arg_1_1 = 4
arg_1 = [arg_1_0,arg_1_1,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(-32,8,[32, 3, 24, 24, 1], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
