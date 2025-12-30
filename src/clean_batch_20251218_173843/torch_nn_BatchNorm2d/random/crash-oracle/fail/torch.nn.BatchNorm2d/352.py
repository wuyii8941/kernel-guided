import torch
arg_1 = 100
arg_2 = False
arg_class = torch.nn.BatchNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-4,2,[16, 151, 10], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
