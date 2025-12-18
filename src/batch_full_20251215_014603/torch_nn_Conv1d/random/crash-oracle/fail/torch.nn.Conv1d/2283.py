import torch
arg_1 = -60.0
arg_2 = -55.0
arg_3 = -56
arg_4 = 37
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-2,16,[0, 16, 50], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
