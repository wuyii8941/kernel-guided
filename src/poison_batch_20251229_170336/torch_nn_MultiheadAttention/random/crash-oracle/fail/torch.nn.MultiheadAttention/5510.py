import torch
arg_1 = 999
arg_2 = 8
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-1024,32768,[1024, 1, 512], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([10, 32, -1, 1], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-2,128,[10, 2147483647, 0], dtype=torch.int16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
