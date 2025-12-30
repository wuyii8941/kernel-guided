import torch
arg_1 = 95
arg_2 = False
arg_class = torch.nn.BatchNorm1d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-128,4,[18, 100], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
