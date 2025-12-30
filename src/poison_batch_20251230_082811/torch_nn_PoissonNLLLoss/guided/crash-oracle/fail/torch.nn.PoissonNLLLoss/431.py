import torch
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.rand([7], dtype=torch.float64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-512,16384,[5], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
