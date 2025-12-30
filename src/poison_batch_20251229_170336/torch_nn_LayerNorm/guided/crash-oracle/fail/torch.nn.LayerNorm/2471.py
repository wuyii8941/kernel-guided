import torch
arg_1 = 2.9805872155325925
arg_2 = 1024.0
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.rand([1, 2, 0, 1], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
