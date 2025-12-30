import torch
arg_1 = 526
arg_2 = 55
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-4,4096,[10, 0, 512], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2,4,[10, 32, 512], dtype=torch.int64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([41, 32, 1, 1], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
