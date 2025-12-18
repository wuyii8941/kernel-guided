import torch
arg_1 = 64
arg_2 = 57
arg_3 = 3
arg_4_0 = 3
arg_4_1 = 3
arg_4_2 = 6
arg_4_3 = 6
arg_4_4 = 0
arg_4_5 = 1
arg_4 = [arg_4_0,arg_4_1,arg_4_2,arg_4_3,arg_4_4,arg_4_5,]
arg_5 = 0.0
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.rand([128, 128, 16, 16], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
