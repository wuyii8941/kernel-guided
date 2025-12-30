import torch
arg_1 = 16
arg_2 = -1
arg_3 = 3
arg_4 = 1
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(0,2,[20, 0, 50, 34], dtype=torch.bool)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
