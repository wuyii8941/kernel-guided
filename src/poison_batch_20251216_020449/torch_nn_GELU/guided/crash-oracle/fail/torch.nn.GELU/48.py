import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-32,1,[5, 16, 64, 69], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
