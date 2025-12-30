import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(0,2,[3, 1], dtype=torch.bool)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([2, -1], dtype=torch.float32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
