import torch
arg_1 = 512
arg_2 = 10
arg_3 = 4.400383570314281
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([10, 0, 1], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2,2,[10, 32, 512], dtype=torch.int64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([18, 32, 512], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
