import torch
arg_1_0 = 3
arg_1_1 = 2
arg_1 = [arg_1_0,arg_1_1,]
arg_2_0 = 2
arg_2_1 = 1
arg_2_2 = 2
arg_2 = [arg_2_0,arg_2_1,arg_2_2,]
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,)
arg_3_0_tensor = torch.rand([20, 16, 50, 32], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
