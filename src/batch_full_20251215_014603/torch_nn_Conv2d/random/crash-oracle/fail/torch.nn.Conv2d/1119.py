import torch
arg_1 = 64
arg_2 = 2
arg_3 = 4
arg_4_0 = 13
arg_4_1 = 51
arg_4_2 = 0
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = -51
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([1, 64, 56, 56], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
