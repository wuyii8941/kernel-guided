import torch
arg_1_tensor = torch.rand([5, 5, 5], dtype=torch.float64)
arg_1 = arg_1_tensor.clone()
arg_2 = -20
arg_3 = -1
arg_4 = 2
res = torch.narrow(arg_1,arg_2,arg_3,arg_4,)
