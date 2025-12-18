import torch
arg_1 = 1536
arg_2 = 2048
arg_3 = 1
arg_4 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,bias=arg_4,)
arg_5_0_tensor = torch.rand([80, 1536, 4, 4], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
