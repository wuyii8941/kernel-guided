import torch
arg_1 = 312
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-16384,2,[20, 0, 10, 10], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
