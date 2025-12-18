import torch
arg_1 = 204
arg_2 = 275
arg_3 = 2
arg_4 = 30
arg_5 = 26
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([1, 0, 44, 80], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
