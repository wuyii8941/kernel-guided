import torch
arg_1 = 16
arg_2 = 33
arg_3 = 35
arg_4_0 = 2
arg_4 = [arg_4_0,]
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-512,32,[0, 16, 50], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
