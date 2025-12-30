import torch
arg_1_tensor = torch.rand([0, 4], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
res = torch.max(arg_1,)
