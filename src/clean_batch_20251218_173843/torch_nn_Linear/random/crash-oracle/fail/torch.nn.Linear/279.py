import torch
arg_1 = 64
arg_2 = 21
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([3, 1024], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
