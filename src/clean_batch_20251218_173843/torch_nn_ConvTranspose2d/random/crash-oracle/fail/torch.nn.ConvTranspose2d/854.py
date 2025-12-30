import torch
arg_1 = False
arg_2 = 1024
arg_3 = 4
arg_4 = -37
arg_5 = -16
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(0,2,[64, 64, 14, 54], dtype=torch.bool)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
