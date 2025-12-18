import torch
arg_1 = 1
arg_2 = 32
arg_3 = True
arg_4 = 1
arg_5 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-4096,16,[32, 1, 5, 17], dtype=torch.int16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
