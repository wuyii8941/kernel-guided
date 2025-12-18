import torch
arg_1 = 512
arg_2 = 1028
arg_3 = -3.9
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-2,64,[10, 32], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([np.int64(1), 25, 509, 1], dtype=torch.complex64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-128,32768,[9, 34], dtype=torch.int32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
