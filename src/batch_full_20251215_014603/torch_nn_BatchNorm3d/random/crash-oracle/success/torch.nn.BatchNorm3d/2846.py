import torch
arg_1 = 100
arg_2 = False
arg_class = torch.nn.BatchNorm3d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-2,4,[20, 158, 35, 45, 0], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
