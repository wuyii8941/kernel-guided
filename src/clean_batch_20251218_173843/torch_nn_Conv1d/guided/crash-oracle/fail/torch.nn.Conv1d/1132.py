import torch
arg_1 = 16
arg_2 = "max"
arg_3 = 3
arg_4_0 = 2
arg_4_1 = 1
arg_4_2 = 1
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-1024,2048,[20, 16, 1], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
