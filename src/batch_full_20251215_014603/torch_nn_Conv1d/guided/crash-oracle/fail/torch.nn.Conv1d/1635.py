import torch
arg_1 = 16
arg_2 = -18
arg_3 = 3
arg_4_0 = 4
arg_4_1 = 2
arg_4 = [arg_4_0,arg_4_1,]
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-256,32,[np.int64(16), 16, np.int64(16)], dtype=torch.int32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
