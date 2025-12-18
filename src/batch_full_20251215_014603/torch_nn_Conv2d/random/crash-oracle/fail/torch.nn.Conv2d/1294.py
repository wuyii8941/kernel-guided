import torch
arg_1 = -1
arg_2 = 1024
arg_3 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([16, 464, 0, 4, 1], dtype=torch.float64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
