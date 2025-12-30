import torch
arg_1_tensor = torch.randint(-16384,128,[2, 2], dtype=torch.int64)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.randint(-8,2,[2, 2], dtype=torch.int64)
arg_2 = arg_2_tensor.clone()
res = torch.gt(arg_1,arg_2,)
