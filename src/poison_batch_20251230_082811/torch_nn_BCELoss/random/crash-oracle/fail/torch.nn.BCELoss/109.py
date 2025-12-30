import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-32,1,[3], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-32768,64,[3, 1], dtype=torch.int16)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
