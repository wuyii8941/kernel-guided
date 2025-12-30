import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-8192,32768,[1, 511, 64, 62], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
