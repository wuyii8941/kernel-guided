import torch
arg_1_0 = -28.0
arg_1_1 = "max"
arg_1_2 = False
arg_1 = [arg_1_0,arg_1_1,arg_1_2,]
arg_2 = 16
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,)
arg_3_0_tensor = torch.rand([16, 288, 30, 30], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
