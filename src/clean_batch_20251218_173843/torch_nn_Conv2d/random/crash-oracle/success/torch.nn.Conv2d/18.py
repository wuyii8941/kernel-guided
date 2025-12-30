import torch
arg_1 = 32
arg_2 = 34
arg_3 = 5
arg_4 = 1
arg_5 = 2
arg_6 = False
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,bias=arg_6,)
arg_7_0_tensor = torch.rand([500, 32, 144, 144], dtype=torch.float32)
arg_7_0 = arg_7_0_tensor.clone()
arg_7 = [arg_7_0,]
res = arg_class(*arg_7)
