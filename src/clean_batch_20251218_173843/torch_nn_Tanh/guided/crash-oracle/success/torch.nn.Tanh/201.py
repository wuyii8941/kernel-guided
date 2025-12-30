import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.randint(-32,8,[83, 1076, 28, 32, 1], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
