import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.randint(-128,1024,[100, 3, 32, 1, 1], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
