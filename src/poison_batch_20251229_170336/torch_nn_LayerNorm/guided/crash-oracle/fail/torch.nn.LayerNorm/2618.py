import torch
arg_1 = 1024
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-2048,2048,[16, 1, 1024], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
