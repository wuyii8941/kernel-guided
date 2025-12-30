import torch
arg_1 = 1
arg_2 = -0.6865878667685124
arg_class = torch.nn.GroupNorm(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-16,1,[20, 16, 10, 10], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
