import torch
arg_1 = -16
arg_class = torch.nn.BatchNorm1d(arg_1,)
arg_2_0_tensor = torch.randint(0,4,[64, 2147483643, 0], dtype=torch.uint8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
