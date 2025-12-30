import torch
arg_1_0 = 2
arg_1_1 = 2
arg_1 = [arg_1_0,arg_1_1,]
arg_2 = -55.0
arg_3_0 = -61
arg_3_1 = 28
arg_3_2 = 1024
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([16, 480, 8, 8], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
