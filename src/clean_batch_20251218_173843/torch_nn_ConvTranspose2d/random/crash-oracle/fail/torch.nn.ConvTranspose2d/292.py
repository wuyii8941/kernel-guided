import torch
arg_1 = 64
arg_2 = 2048
arg_3 = 4
arg_4 = 2
arg_5 = -5
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(0,2,[15, 67, 71, 1], dtype=torch.bool)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
