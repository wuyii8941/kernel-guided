import torch
arg_1 = 77
arg_2 = False
arg_class = torch.nn.BatchNorm3d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-1,4096,[20, 100, 35, 45, 10], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
