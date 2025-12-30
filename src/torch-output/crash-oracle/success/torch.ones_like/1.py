import torch
arg_1_tensor = torch.rand([1], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = torch.preserve_format
res = torch.ones_like(arg_1,memory_format=arg_2,)
