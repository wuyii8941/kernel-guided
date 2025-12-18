import torch
arg_1 = 1054
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.rand([27, 17, 1024], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
