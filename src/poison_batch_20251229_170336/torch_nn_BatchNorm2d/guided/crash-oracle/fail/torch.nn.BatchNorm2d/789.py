import torch
arg_1 = 105
arg_class = torch.nn.BatchNorm2d(arg_1,)
arg_2_0_tensor = torch.rand([16, 960, 4, 4], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
