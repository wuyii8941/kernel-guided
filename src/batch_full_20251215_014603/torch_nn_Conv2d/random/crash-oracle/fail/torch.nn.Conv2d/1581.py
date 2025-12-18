import torch
arg_1 = 512
arg_2 = 512
arg_3 = 14
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,padding=arg_4,)
arg_5_0_tensor = torch.rand([80, 512, 4, 4], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
