import torch
arg_1 = 10
arg_2 = -3
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-1,128,[5, 3, 0], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-128,8,[2, 3], dtype=torch.int32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
