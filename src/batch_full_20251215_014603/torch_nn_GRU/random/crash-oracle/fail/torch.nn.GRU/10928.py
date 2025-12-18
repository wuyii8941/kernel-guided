import torch
arg_1 = 10
arg_2 = 31
arg_3 = -37
arg_class = torch.nn.GRU(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([5, 17], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-16,32768,[2, 3, 23], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
