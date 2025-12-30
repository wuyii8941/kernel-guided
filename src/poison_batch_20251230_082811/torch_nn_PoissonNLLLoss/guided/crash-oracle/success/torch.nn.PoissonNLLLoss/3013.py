import torch
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.rand([], dtype=torch.bfloat16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16384,512,[5, 4], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
