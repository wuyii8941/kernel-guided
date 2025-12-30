import torch
arg_1 = -13
arg_2 = 3
arg_3_0 = -16
arg_3_1 = -36
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 21
arg_5_0 = 21
arg_5_1 = -1024
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([20, 16, 50, 100], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
