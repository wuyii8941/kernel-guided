import torch
arg_1 = 121
arg_2 = -0.4811383284967504
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.rand([512, 6, 128, 4], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
