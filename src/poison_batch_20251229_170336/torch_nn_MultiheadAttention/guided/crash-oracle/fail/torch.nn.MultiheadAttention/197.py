import torch
arg_1 = 507
arg_2 = 8
arg_3 = 0.7132776198912752
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, -1, 1, 0], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-64,4,[10, 32], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([0, 11, 512, 1], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
