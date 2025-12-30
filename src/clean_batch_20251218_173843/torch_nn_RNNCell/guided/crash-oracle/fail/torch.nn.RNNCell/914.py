import torch
arg_1 = 10
arg_2 = 1021
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-4,64,[3], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-1,256,[3, 20], dtype=torch.int64)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
