import torch
arg_1 = -1
arg_2 = 2048
arg_3 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([80, 512, 16, 16], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
