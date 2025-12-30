import torch
arg_1 = 128
arg_class = torch.nn.BatchNorm1d(arg_1,)
arg_2_0_tensor = torch.rand([75, 95], dtype=torch.complex64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
