import torch
arg_1 = 2048
arg_2 = "max"
arg_3 = -6
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([16, 1985, 62, 0], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
