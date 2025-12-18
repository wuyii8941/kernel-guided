import torch
arg_1 = 832
arg_2 = 107
arg_3 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,)
arg_4_0_tensor = torch.rand([80, 832, 4, 4], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
