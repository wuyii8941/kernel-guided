import torch
arg_1 = 32
arg_2 = 3
arg_3 = -16
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,)
arg_5_0_tensor = torch.rand([1, 32, 1082, 1082], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
