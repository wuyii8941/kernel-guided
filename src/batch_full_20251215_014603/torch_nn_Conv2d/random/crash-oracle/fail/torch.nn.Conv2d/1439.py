import torch
arg_1 = 41
arg_2 = 33
arg_3 = -41
arg_4 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.rand([128, 1024, 4, 4], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
