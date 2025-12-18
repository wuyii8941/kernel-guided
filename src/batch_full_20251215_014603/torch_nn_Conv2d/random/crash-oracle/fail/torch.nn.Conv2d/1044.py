import torch
arg_1 = 501
arg_2 = 2
arg_3 = 2
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,)
arg_5_0_tensor = torch.rand([16, 512, 1, 1], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
