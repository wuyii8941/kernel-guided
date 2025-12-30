import torch
arg_1 = 102
arg_2 = False
arg_3 = 4
arg_4 = 2
arg_5 = -8.0
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-2,128,[100, 64, 14, 14], dtype=torch.int16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
