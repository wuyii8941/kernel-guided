import torch
arg_1 = 512
arg_2 = 8
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, 86], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-64,16,[20, 53, 512, 14], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([1, 29, 16], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
