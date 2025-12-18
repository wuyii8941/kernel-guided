import torch
arg_1 = 512
arg_2 = 2048
arg_3 = -20
arg_4 = 1
arg_5 = False
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.rand([32, 512, 56, 56], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
