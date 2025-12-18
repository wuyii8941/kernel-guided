import torch
arg_1 = 10
arg_2 = 7
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([0, 10], dtype=torch.complex64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-32,8,[3, 50], dtype=torch.int8)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
