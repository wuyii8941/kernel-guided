import torch
arg_1 = 1024
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-1,32768,[1, 5], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
