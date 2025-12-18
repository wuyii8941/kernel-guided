import torch
arg_1 = 199
arg_2 = 256
arg_3 = 2
arg_4 = 1
arg_5 = 0
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.randint(-16,4096,[1, 233, 0], dtype=torch.int64)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
