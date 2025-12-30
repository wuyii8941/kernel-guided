import torch
arg_1 = 64
arg_2 = 1
arg_3 = "max"
arg_4_0 = 2
arg_4_1 = 1
arg_4_2 = 2
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = 41
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(0,2,[64, 64, 0, 14], dtype=torch.bool)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
