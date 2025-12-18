import torch
arg_1 = 640
arg_2 = 546
arg_3 = 3
arg_4 = 1
arg_5_0 = 3
arg_5_1 = 3
arg_5_2 = 6
arg_5_3 = 6
arg_5_4 = 0
arg_5_5 = 1
arg_5 = [arg_5_0,arg_5_1,arg_5_2,arg_5_3,arg_5_4,arg_5_5,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([80, 640, 8, 8], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
