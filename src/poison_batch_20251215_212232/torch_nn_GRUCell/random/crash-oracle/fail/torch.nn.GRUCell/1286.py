import torch
arg_1 = 10
arg_2 = 20
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,2,[3, 10, 22], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-16,4,[0, 80], dtype=torch.int64)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
