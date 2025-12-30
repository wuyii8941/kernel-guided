import torch
arg_class = torch.nn.BCEWithLogitsLoss()
arg_1_0_tensor = torch.rand([7], dtype=torch.complex128)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-2048,16384,[], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
