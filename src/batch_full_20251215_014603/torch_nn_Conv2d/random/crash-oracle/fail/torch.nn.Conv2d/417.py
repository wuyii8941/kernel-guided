import torch
arg_1 = 128
arg_2 = 103
arg_3 = 15
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-8,128,[5, 128, 32, 32], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
