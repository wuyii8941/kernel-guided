import torch
arg_1 = 10
arg_2 = -14
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-16384,64,[5, 3, 10, 1], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-128,128,[0, 3], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
