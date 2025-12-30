import torch
arg_1_0 = 312
arg_1 = [arg_1_0,]
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-8192,1,[0, 5, 1024, 1], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
