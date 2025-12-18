import torch
arg_1 = 256
arg_2 = 32
arg_3 = 3
arg_4_0 = 3
arg_4_1 = 1
arg_4 = [arg_4_0,arg_4_1,]
arg_5 = False
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.rand([80, 128, 16, 16], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
