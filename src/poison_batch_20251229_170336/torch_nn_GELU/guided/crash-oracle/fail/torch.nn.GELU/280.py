import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-1,32,[1024, 512, 1, 64], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
