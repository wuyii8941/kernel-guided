import torch
arg_1 = 4.008252086869708
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([16, 5, -1, 7, 65536], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
