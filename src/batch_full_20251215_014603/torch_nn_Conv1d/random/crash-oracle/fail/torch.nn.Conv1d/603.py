import torch
arg_1 = 18
arg_2 = 33
arg_3 = 60
arg_4 = -33
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-4,8,[20, 16, 50, 1], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
