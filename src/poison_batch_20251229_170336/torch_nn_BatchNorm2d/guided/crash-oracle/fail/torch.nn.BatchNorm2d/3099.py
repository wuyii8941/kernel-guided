import torch
arg_1 = -1
arg_2 = True
arg_class = torch.nn.BatchNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(0,2,[21, 100, 11, 47], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
