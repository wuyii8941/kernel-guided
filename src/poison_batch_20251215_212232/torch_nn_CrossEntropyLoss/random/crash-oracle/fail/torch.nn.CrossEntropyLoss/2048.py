import torch
arg_class = torch.nn.CrossEntropyLoss()
arg_1_0_tensor = torch.rand([16, 100], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([16], dtype=torch.complex64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
