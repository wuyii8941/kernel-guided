import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-16384,512,[5, 512, 64, 1, 1], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
