import torch
arg_1 = 16
arg_2 = 16
arg_3 = 3
arg_4 = 2
arg_5_0 = True
arg_5_1 = "max"
arg_5_2 = "mean"
arg_5_3 = -1e+20
arg_5 = [arg_5_0,arg_5_1,arg_5_2,arg_5_3,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([1, 16, 6, 6], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
