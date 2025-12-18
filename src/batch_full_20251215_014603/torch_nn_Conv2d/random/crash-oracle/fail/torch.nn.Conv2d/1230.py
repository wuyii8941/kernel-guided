import torch
arg_1 = -7.0
arg_2 = 100
arg_3 = "mean"
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([128, 1280, 1, 1], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
