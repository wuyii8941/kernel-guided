import torch
arg_1 = 71
arg_2 = 20
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([0, 3], dtype=torch.bfloat16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2048,128,[56, 3, 20, 1], dtype=torch.int64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
