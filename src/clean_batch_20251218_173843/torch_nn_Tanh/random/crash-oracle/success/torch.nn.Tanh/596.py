import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.rand([4, 711], dtype=torch.bfloat16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
