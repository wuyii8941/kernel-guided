import torch
arg_1 = 518
arg_2 = 8
arg_3 = -5.522164414638777
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, 0, 504], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([7, 25], dtype=torch.complex64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-128,128,[10, 32, 518, 1], dtype=torch.int16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
