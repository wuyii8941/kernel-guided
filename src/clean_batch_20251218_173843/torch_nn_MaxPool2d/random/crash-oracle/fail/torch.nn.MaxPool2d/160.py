import torch
arg_1_0 = -26
arg_1_1 = 42
arg_1 = [arg_1_0,arg_1_1,]
arg_2_0 = True
arg_2_1 = 29.0
arg_2 = [arg_2_0,arg_2_1,]
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([1, 512, 22, 40], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
