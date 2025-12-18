import torch
arg_1 = 512
arg_2 = 8
arg_3 = 1.0
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, 58], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-4096,64,[45, 19, 524], dtype=torch.int32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([56, 0, 538], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
