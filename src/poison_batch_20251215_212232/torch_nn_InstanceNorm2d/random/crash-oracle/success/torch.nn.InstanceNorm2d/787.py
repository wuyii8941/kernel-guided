import torch
arg_1 = 88
arg_class = torch.nn.InstanceNorm2d(arg_1,)
arg_2_0_tensor = torch.rand([1, 1, 1, 2], dtype=torch.float64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
