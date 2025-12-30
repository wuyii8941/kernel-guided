import torch
arg_1 = -22
arg_2 = 33
arg_3_0 = 16
arg_3_1 = -31
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = 2
arg_4_1 = 1
arg_4 = [arg_4_0,arg_4_1,]
arg_5_0 = "sum"
arg_5_1 = True
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([15, 16, 50, 62], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
