import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.rand([13, 0, 8, 8], dtype=torch.float64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-128,8,[5, 8, 1], dtype=torch.int16)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
