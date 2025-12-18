import torch
arg_1 = 512
arg_2 = 8
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([np.int64(1024), 69, 512, 1], dtype=torch.float64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([42, 0], dtype=torch.bfloat16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(0,8,[20, 0, 1], dtype=torch.uint8)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
