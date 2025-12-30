import torch
arg_1 = 2
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([18, 13, 7, 2, 7, 13], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
