import torch
arg_1 = 54
arg_2 = 42
arg_3 = -57
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([48, 832, 8], dtype=torch.float64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
