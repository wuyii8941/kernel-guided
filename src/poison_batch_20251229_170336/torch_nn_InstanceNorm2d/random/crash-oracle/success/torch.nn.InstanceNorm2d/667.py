import torch
arg_1 = "max"
arg_class = torch.nn.InstanceNorm2d(arg_1,)
arg_2_0_tensor = torch.randint(0,64,[0, 1, 0, 2], dtype=torch.uint8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
