import torch
arg_1 = 263
arg_2 = 256
arg_3 = 1
arg_4 = "max"
arg_5 = 0
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-8,16384,[0, 256, 44, 80], dtype=torch.int32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
