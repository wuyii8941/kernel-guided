import torch
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.randint(-32768,128,[16, 512, 8, 8], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
