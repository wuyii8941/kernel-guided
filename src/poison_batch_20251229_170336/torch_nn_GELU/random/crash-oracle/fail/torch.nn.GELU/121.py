import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-16384,128,[5, 512, 64, 72], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
