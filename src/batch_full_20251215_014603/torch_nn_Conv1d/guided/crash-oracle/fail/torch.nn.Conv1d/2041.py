import torch
arg_1 = 1e+20
arg_2 = 30
arg_3 = 3
arg_4 = 2
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(0,32,[20, 16, 50, 55], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
