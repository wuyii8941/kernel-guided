import torch
arg_1 = 512
arg_2 = -51
arg_3 = 35.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([10, 36, 524], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2048,32768,[1, 32, 520], dtype=torch.int64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(0,2,[36, 32, 460, 1], dtype=torch.bool)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
