import torch
arg_1 = 487
arg_2 = "reflect"
arg_3 = 3
arg_4 = "max"
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,)
arg_5_0_tensor = torch.rand([80, 512, 2, 2], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
