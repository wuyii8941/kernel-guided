import torch
arg_1 = -65536
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-4096,1024,[0, 17, 1024, 1], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
