import torch
arg_1 = 100
arg_class = torch.nn.InstanceNorm2d(arg_1,)
arg_2_0_tensor = torch.randint(-512,2,[1, 1, 1024, 0], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
