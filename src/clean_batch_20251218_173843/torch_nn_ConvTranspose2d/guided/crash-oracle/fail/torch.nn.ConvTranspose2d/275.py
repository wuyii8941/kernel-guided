import torch
arg_1 = 128
arg_2 = False
arg_3 = 4
arg_4 = -13
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-1,8192,[1024, 64, 32, 14, 1], dtype=torch.int16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
