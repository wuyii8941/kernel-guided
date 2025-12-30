import torch
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.randint(-1,64,[5, 0], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-4096,16,[5, 0], dtype=torch.int16)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
