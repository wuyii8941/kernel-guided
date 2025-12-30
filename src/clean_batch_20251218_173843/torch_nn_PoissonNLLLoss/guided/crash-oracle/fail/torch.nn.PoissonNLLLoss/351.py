import torch
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.randint(-256,8,[5, 2, 1], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-128,256,[63, 2, 1], dtype=torch.int16)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
