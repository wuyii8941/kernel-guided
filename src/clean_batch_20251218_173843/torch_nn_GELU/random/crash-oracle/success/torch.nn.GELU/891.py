import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.rand([7, 512, 71], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
