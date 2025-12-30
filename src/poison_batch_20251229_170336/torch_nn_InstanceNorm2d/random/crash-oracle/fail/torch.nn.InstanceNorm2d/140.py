import torch
arg_1 = 1028
arg_2 = True
arg_class = torch.nn.InstanceNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-4,32768,[1, 32, 1080, 1074], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
