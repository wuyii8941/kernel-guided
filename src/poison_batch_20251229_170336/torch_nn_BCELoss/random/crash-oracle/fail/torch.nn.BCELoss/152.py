import torch
arg_class = torch.nn.BCELoss()
arg_1_0_tensor = torch.randint(-32768,8,[64, 0], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16,16,[0, 0], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
