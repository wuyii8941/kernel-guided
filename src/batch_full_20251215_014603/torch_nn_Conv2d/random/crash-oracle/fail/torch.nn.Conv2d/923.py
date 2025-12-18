import torch
arg_1 = 2106
arg_2 = 135
arg_3_tensor = torch.rand([768], dtype=torch.float32)
arg_3 = arg_3_tensor.clone()
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,bias=arg_3,kernel_size=arg_4,)
arg_5_0_tensor = torch.rand([16, 2048, 6, 6], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
