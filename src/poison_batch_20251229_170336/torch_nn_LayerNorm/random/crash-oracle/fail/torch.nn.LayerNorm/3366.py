import torch
arg_1_0 = 768
arg_1 = [arg_1_0,]
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.rand([1, 0, 1024], dtype=torch.complex128)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
