import torch
arg_1 = -34.0
arg_2 = 16.0
arg_3 = 1024.0
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, 32], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-4,2048,[10, 32, 512, 1], dtype=torch.int32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([0, 0, 539, 0], dtype=torch.complex128)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
