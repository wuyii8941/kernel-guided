import torch
arg_1 = 16
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-256,32768,[20, -1, 10, 10], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
