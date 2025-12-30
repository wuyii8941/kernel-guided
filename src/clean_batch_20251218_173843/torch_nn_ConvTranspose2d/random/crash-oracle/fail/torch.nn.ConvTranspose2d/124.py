import torch
arg_1 = 64
arg_2 = -1024
arg_3_0 = -12
arg_3_1 = 36
arg_3_2 = -20
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = 41
arg_5 = 60
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 64, 14, 14], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
