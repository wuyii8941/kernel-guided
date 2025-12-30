import torch
arg_1 = 558
arg_2 = 2048
arg_3 = -19
arg_4 = 1
arg_5 = False
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,stride=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.randint(-32768,4,[32, 512, 16, 56], dtype=torch.int16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
