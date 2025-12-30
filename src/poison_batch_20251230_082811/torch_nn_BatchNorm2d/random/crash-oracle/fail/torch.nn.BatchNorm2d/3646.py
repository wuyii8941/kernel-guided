import torch
arg_1 = -inf
arg_class = torch.nn.BatchNorm2d(arg_1,)
arg_2_0_tensor = torch.randint(-128,4,[1, 256, 44, 80], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
