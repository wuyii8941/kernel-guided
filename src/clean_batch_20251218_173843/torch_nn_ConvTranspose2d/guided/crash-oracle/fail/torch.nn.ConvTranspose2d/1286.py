import torch
arg_1 = 33
arg_2 = 1
arg_3 = 4
arg_4 = "circular"
arg_5_0 = 3
arg_5_1 = 3
arg_5_2 = 6
arg_5_3 = 6
arg_5_4 = 1
arg_5_5 = 1
arg_5 = [arg_5_0,arg_5_1,arg_5_2,arg_5_3,arg_5_4,arg_5_5,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 64, 14, 14], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
