import torch
arg_1 = 64
arg_2 = 3
arg_3 = "mean"
arg_4 = 2
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(0,1,[100, 64, 14, 14, 60], dtype=torch.uint8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
