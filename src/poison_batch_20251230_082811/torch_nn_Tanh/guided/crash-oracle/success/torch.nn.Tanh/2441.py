import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.randint(-2,2,[64, 3, 33], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
