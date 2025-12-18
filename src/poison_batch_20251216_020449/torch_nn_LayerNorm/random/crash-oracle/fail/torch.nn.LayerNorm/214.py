import torch
arg_1 = 512
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.rand([1024, -1], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
