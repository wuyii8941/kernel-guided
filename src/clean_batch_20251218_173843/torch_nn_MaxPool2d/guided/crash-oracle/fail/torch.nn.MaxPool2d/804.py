import torch
arg_1 = 3
arg_2 = 2
arg_3_0 = 0
arg_3_1 = 4
arg_3_2 = 2
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([128, 384, 30, 30], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
