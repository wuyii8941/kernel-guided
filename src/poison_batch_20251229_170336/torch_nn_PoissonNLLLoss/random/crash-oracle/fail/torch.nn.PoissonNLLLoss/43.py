import torch
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.rand([0, 2], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([0, 1024], dtype=torch.float32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
