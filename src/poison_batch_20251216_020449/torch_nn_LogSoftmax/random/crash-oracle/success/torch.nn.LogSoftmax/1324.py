import torch
arg_class = torch.nn.LogSoftmax()
arg_1_0_tensor = torch.rand([3, 7], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
