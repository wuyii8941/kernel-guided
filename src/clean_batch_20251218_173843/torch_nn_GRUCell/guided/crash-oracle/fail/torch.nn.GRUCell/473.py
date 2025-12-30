import torch
arg_1 = 10
arg_2 = 0
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-16,8,[3, 0, 1], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-2048,8192,[1024, 20], dtype=torch.int64)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
