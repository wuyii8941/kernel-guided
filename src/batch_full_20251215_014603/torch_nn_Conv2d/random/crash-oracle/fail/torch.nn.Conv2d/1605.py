import torch
arg_1 = 620
arg_2 = 640
arg_3 = True
arg_4 = 1
arg_5 = 35
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([80, 640, 8, 8], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
