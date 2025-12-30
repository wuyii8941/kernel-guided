import torch
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.randint(-4,512,[128, 1028, 4, 4, 1], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
