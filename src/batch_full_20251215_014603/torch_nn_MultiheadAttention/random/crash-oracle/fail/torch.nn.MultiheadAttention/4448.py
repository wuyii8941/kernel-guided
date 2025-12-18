import torch
arg_1 = 512
arg_2 = 8
arg_3 = False
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-4,256,[20, np.int64(1), 512], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-4096,32768,[69, 32, 512], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-64,1024,[20, 32, 553], dtype=torch.int64)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
