import torch
arg_class = torch.nn.LogSoftmax()
arg_1_0_tensor = torch.randint(-2048,16,[2, 3], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
