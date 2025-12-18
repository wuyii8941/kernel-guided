import torch
arg_1 = -1
arg_2 = 33
arg_3 = -46
arg_4 = -1e+20
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-8192,128,[20, 16, 50], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
