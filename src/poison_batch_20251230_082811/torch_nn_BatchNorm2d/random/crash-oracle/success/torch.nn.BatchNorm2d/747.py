import torch
arg_1 = 2048
arg_class = torch.nn.BatchNorm2d(arg_1,)
arg_2_0_tensor = torch.randint(0,1,[128, 0, 6, 6], dtype=torch.uint8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
