import torch
arg_1 = 0
arg_2 = 16
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([28, 32], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2,512,[0, 32, 512, 1], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-4,1024,[35, 32, 512, 17], dtype=torch.int16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
