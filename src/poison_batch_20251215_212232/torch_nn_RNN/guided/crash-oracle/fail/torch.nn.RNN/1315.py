import torch
arg_1 = 10
arg_2 = 999
arg_3 = 1024
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-1,128,[8, 3, np.int64(1024)], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-128,32768,[2, 3, 20], dtype=torch.int64)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
