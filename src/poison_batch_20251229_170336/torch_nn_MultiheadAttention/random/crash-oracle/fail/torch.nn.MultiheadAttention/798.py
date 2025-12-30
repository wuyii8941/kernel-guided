import torch
arg_1 = 512
arg_2 = 8
arg_3 = 1.9979986624959456
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(0,2,[20, 32, 512], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([10, 32], dtype=torch.float64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([10, 25, 512], dtype=torch.float16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
