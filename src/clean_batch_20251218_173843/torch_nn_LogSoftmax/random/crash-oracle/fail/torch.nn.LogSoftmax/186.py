import torch
arg_1 = 13
arg_class = torch.nn.LogSoftmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-16384,32,[65, 4, 8, 8], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
