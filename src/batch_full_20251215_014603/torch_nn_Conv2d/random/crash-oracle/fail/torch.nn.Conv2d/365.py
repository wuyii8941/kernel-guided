import torch
arg_1 = 1536
arg_2 = -9
arg_3_tensor = torch.rand([100], dtype=torch.float32)
arg_3 = arg_3_tensor.clone()
arg_4 = 3
arg_class = torch.nn.Conv2d(arg_1,arg_2,bias=arg_3,kernel_size=arg_4,)
arg_5_0_tensor = torch.rand([80, 1536, 7, 7], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
