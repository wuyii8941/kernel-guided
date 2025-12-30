import torch
arg_1 = 2
arg_2_0 = 2
arg_2_1 = 2
arg_2 = [arg_2_0,arg_2_1,]
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,)
arg_3_0_tensor = torch.rand([80, 512, 4, 4], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
