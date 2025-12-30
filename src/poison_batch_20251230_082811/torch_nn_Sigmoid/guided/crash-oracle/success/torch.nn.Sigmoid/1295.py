import torch
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.randint(-1024,1024,[80, 1024, 1], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
