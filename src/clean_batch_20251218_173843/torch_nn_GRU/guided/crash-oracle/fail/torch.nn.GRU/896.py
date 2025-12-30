import torch
arg_1 = 10
arg_2 = 69
arg_3 = -38
arg_class = torch.nn.GRU(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(0,2,[5, 3, 0], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([2, 3, 6], dtype=torch.bfloat16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
