import torch
arg_1_tensor = torch.rand([3, 3], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
res = torch.prod(arg_1,)
