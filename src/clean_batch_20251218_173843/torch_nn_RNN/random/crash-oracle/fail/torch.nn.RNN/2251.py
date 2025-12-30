import torch
arg_1 = 0.0
arg_2 = 20
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([5, 3, 10], dtype=torch.bfloat16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-16,32,[2, 3], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
