import torch
arg_1 = -1e+20
arg_2 = 75
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-1,256,[3, 10], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([3], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
