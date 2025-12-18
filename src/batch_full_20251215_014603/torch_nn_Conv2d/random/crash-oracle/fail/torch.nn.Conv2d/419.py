import torch
arg_1 = 75
arg_2 = -1
arg_3 = 3
arg_4_0 = "max"
arg_4_1 = 1.0
arg_4 = [arg_4_0,arg_4_1,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([1, 64, 9, 9], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
