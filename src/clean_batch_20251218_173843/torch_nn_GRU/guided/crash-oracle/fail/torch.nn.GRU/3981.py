import torch
arg_1 = -29
arg_2 = 20
arg_3 = 2
arg_class = torch.nn.GRU(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-8,16,[0, 3, 10], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,128,[2, 3, 20], dtype=torch.uint8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
