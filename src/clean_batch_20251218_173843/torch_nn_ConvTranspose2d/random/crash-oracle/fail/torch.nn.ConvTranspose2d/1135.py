import torch
arg_1 = False
arg_2 = -34
arg_3 = 4
arg_4 = 2
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([148, 64, 66], dtype=torch.complex64)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
