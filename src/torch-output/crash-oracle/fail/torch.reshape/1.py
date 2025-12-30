import torch
arg_1_tensor = torch.randint(-128,512,[2, 2], dtype=torch.int64)
arg_1 = arg_1_tensor.clone()
arg_2_0 = -56
arg_2 = [arg_2_0,]
res = torch.reshape(arg_1,arg_2,)
