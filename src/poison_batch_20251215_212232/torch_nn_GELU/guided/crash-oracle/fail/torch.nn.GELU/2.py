import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-8,2048,[5, 507, 64, 56], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
