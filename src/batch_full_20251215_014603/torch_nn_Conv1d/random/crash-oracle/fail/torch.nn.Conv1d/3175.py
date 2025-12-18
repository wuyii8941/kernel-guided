import torch
arg_1 = 46.0
arg_2 = 33
arg_3 = 3
arg_4 = -25
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([20, 16, 57], dtype=torch.complex64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
