import torch
arg_1 = 64
arg_2 = 2
arg_3 = 1
arg_4 = 1
arg_5_0 = 1
arg_5_1 = 1
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([51, 64, 31, 28], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
