import torch
arg_1 = -18
arg_2 = nan
arg_class = torch.nn.BatchNorm1d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.rand([999, 100], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
