import torch
arg_1 = 1536
arg_2 = 243
arg_3 = False
arg_4 = 2
arg_class = torch.nn.Conv2d(arg_1,arg_2,bias=arg_3,kernel_size=arg_4,)
arg_5_0_tensor = torch.rand([114, 1536, 0, 38], dtype=torch.float64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
