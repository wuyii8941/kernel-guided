import torch
arg_1 = "reflect"
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([20, 0, 256, -1, 2, 12], dtype=torch.bfloat16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
