import torch
arg_1 = 58
arg_2 = 221
arg_3 = 4
arg_4 = -16
arg_5 = 16
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 64, 14, 14], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
