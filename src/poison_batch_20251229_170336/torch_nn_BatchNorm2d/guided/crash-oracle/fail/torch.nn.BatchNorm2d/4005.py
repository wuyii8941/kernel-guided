import torch
arg_1 = 106
arg_2 = False
arg_class = torch.nn.BatchNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-32768,2048,[14, 96, 999, 16], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
