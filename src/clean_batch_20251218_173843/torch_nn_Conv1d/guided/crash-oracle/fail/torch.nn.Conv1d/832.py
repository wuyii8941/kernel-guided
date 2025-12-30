import torch
arg_1 = 16
arg_2 = 0
arg_3 = 24
arg_4 = 2
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([0, 16, 56], dtype=torch.float16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
