import torch
arg_1 = 512
arg_2 = 8
arg_3 = 61.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-256,256,[20, 22], dtype=torch.int32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([0, 85, 543], dtype=torch.float64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-256,8192,[20, 32, 532], dtype=torch.int32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
