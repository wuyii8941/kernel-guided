import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.rand([100, 3, 41, 57], dtype=torch.complex64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
