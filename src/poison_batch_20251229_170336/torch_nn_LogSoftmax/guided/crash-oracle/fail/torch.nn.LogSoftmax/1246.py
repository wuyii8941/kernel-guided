import torch
arg_1 = 2147483647
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([3, 5], dtype=torch.float16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
