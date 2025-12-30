import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-1024,4,[79, 1], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([39, 1, 1], dtype=torch.complex64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
