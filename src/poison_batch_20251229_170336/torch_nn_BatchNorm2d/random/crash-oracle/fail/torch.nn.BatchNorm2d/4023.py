import torch
arg_1 = 1280
arg_class = torch.nn.BatchNorm2d(arg_1,)
arg_2_0_tensor = torch.rand([15, 1278, 5, 10], dtype=torch.complex128)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
