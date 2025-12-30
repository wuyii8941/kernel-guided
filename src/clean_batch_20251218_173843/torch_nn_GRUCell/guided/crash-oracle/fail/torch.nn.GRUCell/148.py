import torch
arg_1 = 62.0
arg_2 = 20
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,8,[3, 10], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-4,1024,[3, 20], dtype=torch.int32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
