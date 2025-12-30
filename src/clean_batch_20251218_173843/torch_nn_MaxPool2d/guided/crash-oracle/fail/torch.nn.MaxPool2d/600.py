import torch
arg_1_0 = 2
arg_1_1 = 2
arg_1 = [arg_1_0,arg_1_1,]
arg_2 = -42
arg_3 = -6
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([80, 256, 16, 16], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
