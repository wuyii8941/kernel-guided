import torch
arg_1 = -1e+20
arg_2 = 33
arg_3 = 34
arg_4 = True
arg_5 = 0
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([1, 64, 28, 28], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
