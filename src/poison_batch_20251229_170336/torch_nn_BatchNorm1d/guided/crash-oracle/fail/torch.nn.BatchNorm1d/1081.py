import torch
arg_1 = -1e-10
arg_class = torch.nn.BatchNorm1d(arg_1,)
arg_2_0_tensor = torch.rand([96, 256, 1024], dtype=torch.bfloat16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
