import torch
arg_1 = 512
arg_2 = 8
arg_3 = -7.148920166896707
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-1024,1,[20, 32, 504, 0], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,256,[7, 32], dtype=torch.uint8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([6, 32, 518, 1], dtype=torch.float16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
