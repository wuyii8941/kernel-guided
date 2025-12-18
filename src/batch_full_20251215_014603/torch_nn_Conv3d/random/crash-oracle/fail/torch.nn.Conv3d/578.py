import torch
arg_1 = 16
arg_2 = 0
arg_3 = 2
arg_4_0 = 21
arg_4_1 = 31
arg_4_2 = 11
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = 0
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([20, 16, 10, 50, 100], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
