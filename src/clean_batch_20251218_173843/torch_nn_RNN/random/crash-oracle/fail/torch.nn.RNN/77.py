import torch
arg_1 = -46
arg_2 = False
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([5, 3, 3], dtype=torch.complex64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-128,1,[0, 30, 30], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
