import torch
arg_1 = 487
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.rand([20, 1024, 512], dtype=torch.float16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
