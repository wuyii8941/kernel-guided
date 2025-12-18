import torch
arg_1 = 10
arg_2 = 41
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([5, np.int64(1), 0, 1], dtype=torch.complex128)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-1,512,[0, 3, np.int64(16), 1], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
