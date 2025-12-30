import torch
arg_1 = 457
arg_2 = 8
arg_3 = 10.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, 47, 512], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,2,[0, 92], dtype=torch.bool)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-4096,1024,[10, 0, 512], dtype=torch.int16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
