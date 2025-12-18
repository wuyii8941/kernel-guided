import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-4,16,[5, 512, 7, 64], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
