import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-32,32,[64, 1, 1], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16384,8192,[64, 1], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
