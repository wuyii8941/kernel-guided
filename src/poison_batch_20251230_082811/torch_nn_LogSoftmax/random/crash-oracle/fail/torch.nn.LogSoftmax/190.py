import torch
arg_class = torch.nn.LogSoftmax()
arg_1_0_tensor = torch.randint(-2048,2,[2, 11], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
