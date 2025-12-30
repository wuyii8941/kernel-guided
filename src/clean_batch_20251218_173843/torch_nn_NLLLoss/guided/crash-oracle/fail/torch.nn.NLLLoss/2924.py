import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-2,1024,[1, 0, 8, 64], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-128,1,[5, 8, 8], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
