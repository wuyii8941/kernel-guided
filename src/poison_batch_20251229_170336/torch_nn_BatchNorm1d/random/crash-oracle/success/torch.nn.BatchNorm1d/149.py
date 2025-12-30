import torch
arg_1 = 100
arg_2 = True
arg_class = torch.nn.BatchNorm1d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.rand([17, 100], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
