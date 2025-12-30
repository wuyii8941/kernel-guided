import torch
arg_1 = 3
arg_2_0 = -11
arg_2_1 = 17
arg_2 = [arg_2_0,arg_2_1,]
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([1, 64, 41, 128], dtype=torch.float16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
