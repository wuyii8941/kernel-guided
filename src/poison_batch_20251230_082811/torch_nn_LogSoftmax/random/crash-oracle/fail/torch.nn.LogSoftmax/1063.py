import torch
arg_1 = -6
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-512,1024,[1, 5, 1], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
