import torch
arg_1_tensor = torch.rand([3, 2], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
res = torch.rad2deg(arg_1,)
