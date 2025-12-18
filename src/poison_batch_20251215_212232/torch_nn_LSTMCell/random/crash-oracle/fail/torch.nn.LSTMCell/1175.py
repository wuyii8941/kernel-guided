import torch
arg_1 = -11
arg_2 = 22
arg_class = torch.nn.LSTMCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([2, 10], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_0_tensor = torch.rand([2, 20], dtype=torch.float32)
arg_3_1_0 = arg_3_1_0_tensor.clone()
arg_3_1_1_tensor = torch.rand([2, 20], dtype=torch.float32)
arg_3_1_1 = arg_3_1_1_tensor.clone()
arg_3_1 = [arg_3_1_0,arg_3_1_1,]
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
