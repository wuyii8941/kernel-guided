import torch
arg_1 = 64
arg_2 = 6
arg_3 = "mean"
arg_4_0 = 46
arg_4_1 = 55
arg_4 = [arg_4_0,arg_4_1,]
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 64, 14, 14], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
