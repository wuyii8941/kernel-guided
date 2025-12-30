import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.rand([117, 0], dtype=torch.complex64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-64,16,[64, 49], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
