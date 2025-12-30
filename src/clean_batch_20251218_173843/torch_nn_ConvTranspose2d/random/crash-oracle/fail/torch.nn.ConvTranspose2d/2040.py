import torch
arg_1 = 17
arg_2 = 36
arg_3 = 4
arg_4 = 2
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-32768,2048,[64, 64, 14, 63], dtype=torch.int32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
