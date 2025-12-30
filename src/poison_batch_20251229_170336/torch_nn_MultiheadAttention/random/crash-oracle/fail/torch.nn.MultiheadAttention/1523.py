import torch
arg_1 = "replicate"
arg_2 = 3
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([10, 0, 512, 1], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2048,128,[0, -1, 504], dtype=torch.int32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-128,16384,[10, 32, 16, 0], dtype=torch.int64)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
