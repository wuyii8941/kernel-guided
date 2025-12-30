import torch
arg_1 = 1023
arg_class = torch.nn.BatchNorm1d(arg_1,)
arg_2_0_tensor = torch.randint(-32,4,[106, 1024, 11], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
