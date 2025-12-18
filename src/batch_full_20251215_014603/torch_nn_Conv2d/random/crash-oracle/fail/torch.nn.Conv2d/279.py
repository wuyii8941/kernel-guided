import torch
arg_1 = 512
arg_2 = 2048
arg_3 = 16
arg_4 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.rand([0, 512, 16, 16], dtype=torch.complex128)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
