import torch
arg_1 = 192
arg_class = torch.nn.BatchNorm2d(arg_1,)
arg_2_0_tensor = torch.rand([128, 13, 30, 35], dtype=torch.complex128)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
