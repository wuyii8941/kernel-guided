import torch
arg_1 = "max"
arg_2 = 512
arg_3 = 3
arg_4 = -36
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,padding=arg_4,)
arg_5_0_tensor = torch.rand([5, 512, 4, 6, 13], dtype=torch.complex64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
