import torch
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.randint(0,2,[5, 2], dtype=torch.bool)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(0,1,[5, 2], dtype=torch.uint8)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
