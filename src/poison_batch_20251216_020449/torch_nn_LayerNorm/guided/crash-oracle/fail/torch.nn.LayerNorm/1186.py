import torch
arg_1 = 1025
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(0,2,[1024, -1, 1028], dtype=torch.bool)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
