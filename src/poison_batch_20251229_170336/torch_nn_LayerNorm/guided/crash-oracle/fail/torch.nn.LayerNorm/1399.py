import torch
arg_1 = 1
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-4,128,[12, 7, 0], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
