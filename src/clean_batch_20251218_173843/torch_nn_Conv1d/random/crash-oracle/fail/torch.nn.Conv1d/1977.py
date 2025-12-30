import torch
arg_1 = 58
arg_2 = 33
arg_3 = 23
arg_4 = -33
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-128,1,[20, 16], dtype=torch.int32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
