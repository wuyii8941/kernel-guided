import torch
arg_1 = 16
arg_2 = 33
arg_3_0 = 25
arg_3_1 = -20
arg_3_2 = 44
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = -49
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-32768,256,[71, 16], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
