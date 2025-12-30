import torch
arg_1 = -5
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-8192,1024,[3, 7], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
