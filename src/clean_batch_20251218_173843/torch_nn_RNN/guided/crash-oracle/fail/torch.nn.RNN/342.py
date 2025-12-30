import torch
arg_1 = 26
arg_2 = 20
arg_3 = -1e+20
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-16384,512,[49, 3, 10], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([2, 3, 20], dtype=torch.complex128)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
