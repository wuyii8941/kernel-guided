import torch
arg_1 = -1
arg_2 = 32
arg_3 = -20
arg_4_0 = 0
arg_4_1 = 4
arg_4_2 = 2
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_tensor = torch.rand([64], dtype=torch.float32)
arg_5 = arg_5_tensor.clone()
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.rand([16, 128, 32, 32], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
