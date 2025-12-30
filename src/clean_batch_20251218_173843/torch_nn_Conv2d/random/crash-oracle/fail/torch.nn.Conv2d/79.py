import torch
arg_1 = 512
arg_2 = 2048
arg_3 = -51
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-128,16,[16, 512, 16], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
