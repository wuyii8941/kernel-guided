import torch
arg_1 = 5.101914362748462
arg_2 = 6
arg_class = torch.nn.GroupNorm(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([12, 6, 10], dtype=torch.complex64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
