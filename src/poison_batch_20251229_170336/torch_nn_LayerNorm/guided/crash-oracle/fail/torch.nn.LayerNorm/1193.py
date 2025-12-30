import torch
arg_1 = 121
arg_2 = 1e-12
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.rand([512, 10, 121], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
