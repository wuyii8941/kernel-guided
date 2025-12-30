import torch
arg_1 = 58
arg_2 = 21
arg_3 = 55
arg_4 = 51
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 64, 14, 0], dtype=torch.float16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
