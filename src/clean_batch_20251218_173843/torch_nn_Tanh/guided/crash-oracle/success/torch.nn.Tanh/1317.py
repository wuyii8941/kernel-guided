import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.randint(-128,512,[3], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
