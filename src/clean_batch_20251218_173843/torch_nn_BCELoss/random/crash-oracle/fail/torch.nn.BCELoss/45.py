import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-8192,2048,[64, 1, 63], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([36, 1, 0], dtype=torch.float32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
