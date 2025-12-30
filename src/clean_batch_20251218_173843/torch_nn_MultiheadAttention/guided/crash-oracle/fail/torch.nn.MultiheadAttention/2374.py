import torch
arg_1 = 512
arg_2 = 8
arg_3 = False
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([77, 32], dtype=torch.bfloat16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-16,1,[3, 67, 512], dtype=torch.int64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([10, 26, 519], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
