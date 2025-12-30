import torch
arg_1 = 92
arg_2 = False
arg_class = torch.nn.BatchNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.rand([14, 100, 35, 16], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
