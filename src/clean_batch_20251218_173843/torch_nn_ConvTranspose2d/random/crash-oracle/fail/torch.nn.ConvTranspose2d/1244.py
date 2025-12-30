import torch
arg_1 = True
arg_2 = 1
arg_3 = -12
arg_4 = -63.0
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-2048,256,[99, 64, 14, 14], dtype=torch.int32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
