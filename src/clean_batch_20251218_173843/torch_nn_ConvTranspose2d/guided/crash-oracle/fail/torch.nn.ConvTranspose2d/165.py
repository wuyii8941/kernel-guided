import torch
arg_1 = 64
arg_2 = 3
arg_3 = 4
arg_4 = 61
arg_5 = "circular"
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([112, 64, 14, 0], dtype=torch.complex64)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
