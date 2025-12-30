import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-16,128,[5, 512, 123, 75], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
