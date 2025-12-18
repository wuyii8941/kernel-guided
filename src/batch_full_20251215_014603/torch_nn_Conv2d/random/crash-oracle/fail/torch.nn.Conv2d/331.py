import torch
arg_1 = 2048
arg_2 = 33
arg_3_0 = -16
arg_3_1 = 27
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([128, 2048, 2, 2], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
