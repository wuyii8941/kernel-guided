import torch
arg_1 = 10
arg_2 = False
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,256,[3, 10, 1], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([3, 81, 1], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
