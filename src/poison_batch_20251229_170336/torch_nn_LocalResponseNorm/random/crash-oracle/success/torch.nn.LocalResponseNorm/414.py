import torch
arg_1 = None
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.randint(-16384,16,[0, 5, 26, 24], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
