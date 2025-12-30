import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-256,256,[16, 4, 8, 7, 1], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-2048,16,[5, 6, 8], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
