import torch
arg_1_tensor = torch.rand([5, 5, 5], dtype=torch.complex128)
arg_1 = arg_1_tensor.clone()
arg_2 = -22
arg_3_0 = 0
arg_3_1 = 1
arg_3 = [arg_3_0,arg_3_1,]
res = torch.rot90(arg_1,arg_2,arg_3,)
