import torch
arg_1 = -36
arg_2_0 = 2
arg_2 = [arg_2_0,]
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([1, 75, 136], dtype=torch.float16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
