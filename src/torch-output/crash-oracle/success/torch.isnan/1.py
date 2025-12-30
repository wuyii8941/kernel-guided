import torch
arg_1_tensor = torch.rand([5, 5, 5], dtype=torch.complex128)
arg_1 = arg_1_tensor.clone()
res = torch.isnan(arg_1,)
