import torch
arg_1 = -31.0
arg_2 = 9
arg_3_0 = -37
arg_3_1 = 1024
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = 57
arg_4_1 = 49
arg_4 = [arg_4_0,arg_4_1,]
arg_5_0 = 1
arg_5_1 = 1
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([100, 32, 85, 85], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
