import torch
arg_1 = True
arg_2 = 20
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([51], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-8,512,[0, 20], dtype=torch.int16)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
