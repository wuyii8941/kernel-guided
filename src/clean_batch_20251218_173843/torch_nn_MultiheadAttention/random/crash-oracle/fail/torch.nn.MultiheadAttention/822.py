import torch
arg_1 = "max"
arg_2 = 14
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([10, 32, 500, 0], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-512,8192,[91, 12, 0, 1], dtype=torch.int64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-16,16384,[10, 0, 484, 0], dtype=torch.int64)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
