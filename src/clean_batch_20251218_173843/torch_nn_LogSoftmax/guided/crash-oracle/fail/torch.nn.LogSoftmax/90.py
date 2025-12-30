import torch
arg_1 = 38
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([24, 52, 43, 54, 1], dtype=torch.float64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
