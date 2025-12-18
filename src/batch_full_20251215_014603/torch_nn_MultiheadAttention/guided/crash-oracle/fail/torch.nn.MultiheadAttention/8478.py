import torch
arg_1 = 512
arg_2 = 8
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([62, 32, 512], dtype=torch.complex64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,4,[10, 32, 527], dtype=torch.uint8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([10, 47, 567, 1], dtype=torch.complex128)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
