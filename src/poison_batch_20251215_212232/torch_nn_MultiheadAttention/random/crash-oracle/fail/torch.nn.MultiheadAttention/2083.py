import torch
arg_1 = 512
arg_2 = 8
arg_3 = -3.207220683876265
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(0,8,[20, 56], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,2,[10, 32], dtype=torch.bool)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-4,16,[10, 32, 512, 1], dtype=torch.int8)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
