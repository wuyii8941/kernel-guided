import torch
arg_1 = -40
arg_2 = 20
arg_class = torch.nn.LSTMCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([16, 10], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_0_tensor = torch.randint(-256,8192,[36], dtype=torch.int64)
arg_3_1_0 = arg_3_1_0_tensor.clone()
arg_3_1_1_tensor = torch.rand([2, 81, 0], dtype=torch.float32)
arg_3_1_1 = arg_3_1_1_tensor.clone()
arg_3_1 = [arg_3_1_0,arg_3_1_1,]
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
