import torch
arg_1_0 = "max"
arg_1_1 = "max"
arg_1 = [arg_1_0,arg_1_1,]
arg_2_0 = 2
arg_2_1 = 1
arg_2 = [arg_2_0,arg_2_1,]
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,2,[63, 256, 60, 16, 1], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
