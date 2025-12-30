import torch
arg_1 = 71
arg_2 = 20
arg_3 = -18
arg_class = torch.nn.GRU(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([0, 3, 54], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,2,[2, 3, 0], dtype=torch.bool)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
