import torch
arg_1 = 64
arg_2 = 3
arg_3 = 4
arg_4 = 2
arg_5 = -33
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-4,128,[19, 0, 14, 14], dtype=torch.int8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
