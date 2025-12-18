import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-64,128,[64, 65536, 0], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-2048,4,[0, 1], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
