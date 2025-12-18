import torch
arg_1 = 1024.0
arg_2 = 16
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,2,[3, np.int64(1024)], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-2048,256,[10, 20], dtype=torch.int64)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
