import torch
arg_1 = 77
arg_2 = 1
arg_3 = 4
arg_4 = 0
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(0,16,[64, 64, 78], dtype=torch.uint8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
