import torch
arg_1_0 = 1024
arg_1 = [arg_1_0,]
arg_2 = 1e-12
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.randint(0,2,[3, 6, 384, 1], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
