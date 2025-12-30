import torch
arg_1 = 512
arg_2 = -15
arg_3 = -37.9
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, 32, 500], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-512,8,[13, 93, 512, 1], dtype=torch.int32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([66, 0, 533], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
