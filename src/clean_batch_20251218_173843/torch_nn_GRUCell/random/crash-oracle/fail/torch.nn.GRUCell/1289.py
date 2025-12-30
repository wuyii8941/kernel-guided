import torch
arg_1 = 10
arg_2 = -84
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([3, 1], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([3, 0], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
