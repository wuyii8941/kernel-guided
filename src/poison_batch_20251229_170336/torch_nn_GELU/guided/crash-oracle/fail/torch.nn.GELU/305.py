import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(0,2,[5, 518, 1, 16], dtype=torch.bool)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
