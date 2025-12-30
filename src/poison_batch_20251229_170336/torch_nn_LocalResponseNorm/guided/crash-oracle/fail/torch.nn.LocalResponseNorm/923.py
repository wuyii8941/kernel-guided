import torch
arg_1_0 = 2
arg_1_1 = 1
arg_1_2 = 1
arg_1_3 = 2
arg_1 = [arg_1_0,arg_1_1,arg_1_2,arg_1_3,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(0,64,[31, 5, 24, 24], dtype=torch.uint8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
