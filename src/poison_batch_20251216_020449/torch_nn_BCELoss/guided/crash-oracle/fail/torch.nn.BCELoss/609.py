import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-32,256,[64, 65536], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([256, 1], dtype=torch.complex128)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
