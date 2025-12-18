import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.rand([2, 7, 57, 0], dtype=torch.complex128)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
