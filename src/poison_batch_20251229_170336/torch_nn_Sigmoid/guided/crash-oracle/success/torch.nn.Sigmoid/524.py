import torch
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.rand([16, 256, 23, 16, 1], dtype=torch.complex128)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
