import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-128,512,[64, 65541], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-4096,8192,[64, 1, 1], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
