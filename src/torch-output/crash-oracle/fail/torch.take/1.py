import torch
arg_1_tensor = torch.rand([], dtype=torch.float64)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([0], dtype=torch.float16)
arg_2 = arg_2_tensor.clone()
res = torch.take(arg_1,arg_2,)
