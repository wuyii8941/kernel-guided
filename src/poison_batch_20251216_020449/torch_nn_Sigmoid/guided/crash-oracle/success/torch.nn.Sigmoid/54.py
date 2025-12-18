import torch
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.randint(-32768,32768,[0, 1024, 4, 7, 1], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
