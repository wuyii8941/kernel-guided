import torch
arg_1_0 = 1
arg_1_1 = 30
arg_1 = [arg_1_0,arg_1_1,]
arg_2_0 = -28
arg_2_1 = -16
arg_2 = [arg_2_0,arg_2_1,]
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-128,4,[1, 296, 8, 74], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
