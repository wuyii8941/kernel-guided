import torch
arg_1 = 41
arg_2 = 20
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([0, 36, 1], dtype=torch.float64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-1,4096,[3, 20, 1], dtype=torch.int32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
