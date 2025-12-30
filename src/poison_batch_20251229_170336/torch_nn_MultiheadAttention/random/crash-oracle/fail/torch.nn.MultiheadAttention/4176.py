import torch
arg_1 = 512
arg_2 = 8
arg_3 = inf
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-2048,256,[10, 32], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2,1024,[9, 32], dtype=torch.int32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-4096,2048,[16, -1, 0], dtype=torch.int64)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
