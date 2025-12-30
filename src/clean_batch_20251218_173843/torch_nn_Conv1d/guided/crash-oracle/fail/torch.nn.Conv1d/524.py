import torch
arg_1 = 16
arg_2 = 24
arg_3 = -1024
arg_4 = -5.0
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-256,128,[20, 16, 1], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
