import torch
arg_1 = -1024.0
arg_2 = 4
arg_3 = 43
arg_4 = 1
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(0,2,[20, 14, np.int64(16), 0], dtype=torch.bool)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
