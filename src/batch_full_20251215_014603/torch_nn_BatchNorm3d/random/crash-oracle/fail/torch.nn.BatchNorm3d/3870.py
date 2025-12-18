import torch
arg_1 = -16
arg_2 = 35.0
arg_class = torch.nn.BatchNorm3d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(0,2,[0, 100, 35, 45, 10], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
