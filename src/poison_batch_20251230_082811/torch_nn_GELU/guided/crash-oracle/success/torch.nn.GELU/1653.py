import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.rand([16, 512, 65], dtype=torch.float64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
