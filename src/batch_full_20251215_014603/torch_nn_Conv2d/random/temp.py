import torch
arg_1 = 240
arg_2 = 960
arg_3 = 1024
arg_4 = 3
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,groups=arg_4,)
arg_5_0_tensor = torch.rand([16, 240, 4, 4], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
