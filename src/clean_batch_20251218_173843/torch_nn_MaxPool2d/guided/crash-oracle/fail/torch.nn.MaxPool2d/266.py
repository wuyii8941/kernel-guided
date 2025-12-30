import torch
arg_1 = 3
arg_2 = 61
arg_3 = 6
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([16, 728, 8, 8], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
