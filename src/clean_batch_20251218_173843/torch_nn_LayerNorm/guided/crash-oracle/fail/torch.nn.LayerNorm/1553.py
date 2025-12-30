import torch
arg_1 = 1024
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-16384,128,[32, 5, 1086], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
