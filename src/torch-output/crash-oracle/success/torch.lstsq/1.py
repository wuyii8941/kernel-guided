import torch
arg_1_tensor = torch.rand([5, 2], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([5, 3], dtype=torch.float32)
arg_2 = arg_2_tensor.clone()
res = torch.lstsq(arg_1,arg_2,)
