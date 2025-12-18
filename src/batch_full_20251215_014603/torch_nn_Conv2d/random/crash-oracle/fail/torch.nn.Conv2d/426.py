import torch
arg_1 = 256
arg_2 = 1.0
arg_3 = -47
arg_4 = 1
arg_5 = 0
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([1, 256, 8, 64], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
