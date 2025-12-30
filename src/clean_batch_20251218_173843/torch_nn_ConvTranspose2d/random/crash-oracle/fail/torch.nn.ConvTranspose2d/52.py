import torch
arg_1 = 0.0
arg_2 = 960
arg_3 = 4
arg_4 = 2
arg_5 = -47
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-32,1,[64, 64, 14, 14, 1], dtype=torch.int16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
