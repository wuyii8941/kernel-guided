import torch
arg_1_0 = 3
arg_1_1 = 5
arg_1_2 = 2
arg_1 = [arg_1_0,arg_1_1,arg_1_2,]
arg_2 = 2
arg_3 = -16
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([128, 88, 32, 32], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
