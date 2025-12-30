import torch
arg_1 = 1024
arg_2 = 16
arg_3 = False
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-32,128,[20, 32, 513], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([-1, 32, 512], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([8, 32, 1], dtype=torch.complex128)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
