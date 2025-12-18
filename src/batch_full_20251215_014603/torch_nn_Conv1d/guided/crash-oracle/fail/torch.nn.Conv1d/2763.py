import torch
arg_1 = 16
arg_2 = 33
arg_3_0 = -16
arg_3_1 = -1
arg_3_2 = -16
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = 2
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-256,32768,[20, 16, 50], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
