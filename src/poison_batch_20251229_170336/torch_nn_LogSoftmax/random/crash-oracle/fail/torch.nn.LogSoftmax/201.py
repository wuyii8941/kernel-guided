import torch
arg_1_0 = -999
arg_1_1 = 9
arg_1 = [arg_1_0,arg_1_1,]
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([5, 4, 8, 8], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
