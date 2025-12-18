import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.rand([8, 16, 64, 56, 0], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
