import torch
arg_1 = 2
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([38, 5, 0, 0], dtype=torch.bfloat16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
