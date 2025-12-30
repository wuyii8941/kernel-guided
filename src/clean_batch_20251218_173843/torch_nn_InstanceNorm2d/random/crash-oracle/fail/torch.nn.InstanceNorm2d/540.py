import torch
arg_1 = 102
arg_2 = True
arg_class = torch.nn.InstanceNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.rand([5, 64, 64, 64], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
