import torch
arg_1 = -88
arg_2 = True
arg_class = torch.nn.InstanceNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-8,1,[0, 52, 1080], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
