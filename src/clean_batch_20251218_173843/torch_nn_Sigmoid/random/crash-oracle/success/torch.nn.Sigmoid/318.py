import torch
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.randint(-16,128,[128, 1024], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
