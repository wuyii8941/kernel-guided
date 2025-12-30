import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.randint(-128,2,[122, 16, 68, 61], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
