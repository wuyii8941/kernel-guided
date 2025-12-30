import torch
arg_1 = 16
arg_2 = 16
arg_3_0 = -6
arg_3_1 = -56
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = 2
arg_4_1 = 1
arg_4 = [arg_4_0,arg_4_1,]
arg_5_0 = -49
arg_5_1 = -17
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([20, 71, 50], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
