import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-128,32,[], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
