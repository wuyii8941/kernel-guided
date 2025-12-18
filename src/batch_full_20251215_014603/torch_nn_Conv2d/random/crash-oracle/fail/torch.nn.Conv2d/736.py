import torch
arg_1 = 3
arg_2 = 64
arg_3 = 4
arg_4 = 16
arg_5 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([0, 60, 28, 28], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
