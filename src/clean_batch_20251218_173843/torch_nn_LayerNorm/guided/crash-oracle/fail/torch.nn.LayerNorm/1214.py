import torch
arg_1 = 78.0
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-4,8,[1, 1, 1016, 1], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
