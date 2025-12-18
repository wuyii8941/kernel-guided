import torch
arg_1 = 512
arg_2 = -1024
arg_3 = 2
arg_4 = 1
arg_5_0 = 16
arg_5_1 = 0
arg_5_2 = 1
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([1, 256, 8, 16], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
