import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-8,8,[5, 0, 6, 8], dtype=torch.int8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16384,16,[5, 16], dtype=torch.int16)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
