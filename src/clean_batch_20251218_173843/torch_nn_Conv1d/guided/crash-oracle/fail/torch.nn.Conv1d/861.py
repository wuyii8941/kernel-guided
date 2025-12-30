import torch
arg_1 = 16
arg_2 = 0
arg_3_0 = 2
arg_3_1 = 2
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 41
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([20, 16, 50], dtype=torch.bfloat16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
