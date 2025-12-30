import torch
arg_1 = 40
arg_2 = 987
arg_3 = 101
arg_class = torch.nn.GRU(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(0,4,[5, 0, 10], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([0, 3], dtype=torch.float64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
