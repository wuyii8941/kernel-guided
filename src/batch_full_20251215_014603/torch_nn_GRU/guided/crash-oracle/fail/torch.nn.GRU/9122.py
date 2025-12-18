import torch
arg_1 = 10
arg_2 = 20
arg_3 = 2
arg_class = torch.nn.GRU(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-128,1024,[0, 3, 10], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-4,256,[64, 3, 0], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
