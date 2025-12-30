import torch
arg_1 = 27
arg_2 = 4
arg_3 = 36
arg_4_0 = -41
arg_4 = [arg_4_0,]
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([20, 16, 50], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
