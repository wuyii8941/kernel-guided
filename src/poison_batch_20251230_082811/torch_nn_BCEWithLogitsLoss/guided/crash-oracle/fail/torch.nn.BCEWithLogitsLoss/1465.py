import torch
arg_class = torch.nn.BCEWithLogitsLoss()
arg_1_0_tensor = torch.randint(-4,2048,[3], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-8,32768,[3], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
