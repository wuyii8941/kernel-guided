import torch
arg_1 = 1
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-64,16384,[0, 0, 8, 45, 1], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
