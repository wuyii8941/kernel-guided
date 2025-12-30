import torch
arg_1 = 2
arg_class = torch.nn.InstanceNorm2d(arg_1,)
arg_2_0_tensor = torch.randint(-2,256,[1, 1, 1, 0, 1], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
