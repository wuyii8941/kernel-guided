import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.rand([3, 16, 64, 71, 0], dtype=torch.bfloat16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
