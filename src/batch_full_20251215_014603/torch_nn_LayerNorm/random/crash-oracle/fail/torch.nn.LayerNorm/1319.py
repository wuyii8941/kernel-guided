import torch
arg_1 = 539
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-8,32768,[20, 0, 512], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
