import torch
arg_1 = "mean"
arg_class = torch.nn.InstanceNorm2d(arg_1,)
arg_2_0_tensor = torch.randint(-4096,256,[1, 0, 44, 2], dtype=torch.int32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
