import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(0,2,[3, 5], dtype=torch.bool)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-8192,512,[3], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
