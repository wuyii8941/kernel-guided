import torch
arg_1 = True
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-8,16384,[1, 0, 1024], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
