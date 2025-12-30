import torch
arg_1 = 10
arg_2 = -14.0
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([3, 0, 1], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-32,32768,[3, 0], dtype=torch.int16)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
