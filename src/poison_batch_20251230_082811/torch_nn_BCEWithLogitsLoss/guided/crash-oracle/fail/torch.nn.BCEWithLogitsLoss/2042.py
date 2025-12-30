import torch
arg_class = torch.nn.BCEWithLogitsLoss()
arg_1_0_tensor = torch.randint(-1024,1,[], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-8,8192,[], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
