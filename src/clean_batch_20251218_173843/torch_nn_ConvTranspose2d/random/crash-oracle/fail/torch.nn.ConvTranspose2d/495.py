import torch
arg_1 = 64
arg_2 = 8
arg_3 = -12
arg_4 = 2
arg_5_0 = 1
arg_5_1 = 1
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([11, 64, 14], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
