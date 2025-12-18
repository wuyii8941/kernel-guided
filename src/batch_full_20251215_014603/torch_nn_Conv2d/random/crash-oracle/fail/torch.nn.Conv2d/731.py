import torch
arg_1 = 64
arg_2 = 42
arg_3 = 1
arg_4 = 1
arg_5 = 29
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([1, 19, 65, 28], dtype=torch.complex128)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
