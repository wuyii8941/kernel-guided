import torch
arg_1 = 74.0
arg_2 = -22
arg_3 = 3
arg_4 = 101.0
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.rand([np.int64(1), 16, 50], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
