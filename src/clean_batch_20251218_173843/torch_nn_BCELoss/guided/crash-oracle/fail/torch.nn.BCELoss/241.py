import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.rand([64, 29, 1], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16,32,[64, 0], dtype=torch.int8)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
