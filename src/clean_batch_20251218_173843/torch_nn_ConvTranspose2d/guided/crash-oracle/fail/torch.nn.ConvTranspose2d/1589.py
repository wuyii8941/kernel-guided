import torch
arg_1 = False
arg_2 = 1040
arg_3_0 = True
arg_3_1 = 86.0
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 2
arg_5 = 44
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 64, 14, 14], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
