import torch
arg_1 = 16
arg_2 = 16
arg_3 = 37
arg_4 = 2
arg_5_0 = 4
arg_5_1 = 2
arg_5_2 = 0
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.randint(-1,64,[16, 16, 69, 6], dtype=torch.int8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
