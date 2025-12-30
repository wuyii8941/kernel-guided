import torch
arg_1 = 256
arg_class = torch.nn.BatchNorm1d(arg_1,)
arg_2_0_tensor = torch.randint(-512,8192,[0, 7], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
