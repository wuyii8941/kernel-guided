import torch
arg_1 = 1
arg_2 = -2.3015052462643446
arg_class = torch.nn.GroupNorm(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([28, 0, 10, 10], dtype=torch.float64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
