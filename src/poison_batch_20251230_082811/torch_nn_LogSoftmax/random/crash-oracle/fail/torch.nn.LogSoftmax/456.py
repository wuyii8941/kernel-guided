import torch
arg_1 = 1024
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-1024,512,[5, 4, 8, 16], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
