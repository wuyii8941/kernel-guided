import torch
arg_1 = 468
arg_2 = 8
arg_3 = 36.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([10, 54], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-8,256,[0, 32], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([10, 32, 448], dtype=torch.complex64)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
