import torch
arg_1 = 1084
arg_2 = 2048
arg_3_0 = 2
arg_3_1 = 2
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 59.0
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.rand([16, 1024, 8, 8], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
