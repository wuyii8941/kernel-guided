import torch
arg_1 = 512
arg_2 = 8
arg_3 = -38.9
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(0,2,[10, 32, 512, 3], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([10, 69, 512], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([0, 1024, 0], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
