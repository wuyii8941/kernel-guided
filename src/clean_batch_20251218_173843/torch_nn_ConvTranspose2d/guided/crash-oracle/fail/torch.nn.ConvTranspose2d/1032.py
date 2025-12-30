import torch
arg_1 = 64
arg_2 = 3
arg_3 = 3
arg_4_0 = 4
arg_4_1 = 2
arg_4 = [arg_4_0,arg_4_1,]
arg_5 = 1052.0
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 64, 16, 14, 1], dtype=torch.float64)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
