import torch
arg_1 = 9
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(0,2,[16, 5, 16, 7, 7, 34], dtype=torch.bool)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
