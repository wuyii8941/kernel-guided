import torch
arg_1 = -1e-10
arg_2 = 5
arg_3 = 3.847164227137307
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-8192,1024,[10, 32, 508], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([3, 32, 512], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([10, -1, 512], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
