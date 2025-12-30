import torch
arg_1 = 22.0
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(-128,64,[1024, 5, 51, 7, 0, 64, 1], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
