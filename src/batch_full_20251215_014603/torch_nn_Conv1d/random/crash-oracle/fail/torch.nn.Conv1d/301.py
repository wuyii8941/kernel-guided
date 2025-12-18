import torch
arg_1 = 0
arg_2 = 88
arg_3 = 7
arg_4 = 2
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-16,32,[20, 16, 50], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
