import torch
arg_1 = 16
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-32,64,[20, 5, 1, 10], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
