import torch
arg_1 = -11
arg_2 = 12544
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([64, 32], dtype=torch.complex64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
