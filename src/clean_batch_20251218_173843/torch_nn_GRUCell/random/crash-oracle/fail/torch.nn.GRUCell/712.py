import torch
arg_1 = 1024
arg_2 = -55.0
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-16,8192,[3, 0, 1], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([3, 51], dtype=torch.complex64)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
