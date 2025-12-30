import torch
arg_1 = 64
arg_2 = 35
arg_3 = -47
arg_4 = 2
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-4096,512,[112, 64, 14, 14, 1], dtype=torch.int64)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
