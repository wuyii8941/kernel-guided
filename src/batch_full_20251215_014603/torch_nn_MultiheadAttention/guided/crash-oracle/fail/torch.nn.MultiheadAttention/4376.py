import torch
arg_1 = 0
arg_2 = 8
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-512,16,[np.int64(16), 32, 0], dtype=torch.int32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([10, 67, 512], dtype=torch.bfloat16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-2048,16384,[0, 32, 518], dtype=torch.int32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
