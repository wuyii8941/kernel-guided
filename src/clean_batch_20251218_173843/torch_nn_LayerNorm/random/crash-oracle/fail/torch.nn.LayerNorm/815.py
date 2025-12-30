import torch
arg_1 = -29
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-128,512,[20, 0, 10, 37], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
