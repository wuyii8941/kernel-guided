import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-4,8192,[0, 512, 64, 7], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
