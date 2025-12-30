import torch
arg_1 = 1071.0
arg_2 = 20
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-2,8,[3, 10], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([0, 20], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
