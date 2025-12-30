import torch
arg_1_tensor = torch.rand([128, 960, 4, 4], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([128, 960, 4, 4], dtype=torch.float32)
arg_2 = arg_2_tensor.clone()
res = torch.add(arg_1,arg_2,)
