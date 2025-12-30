import torch
arg_1 = 768
arg_2 = 63.000000000001
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.rand([3, 6, 768], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
