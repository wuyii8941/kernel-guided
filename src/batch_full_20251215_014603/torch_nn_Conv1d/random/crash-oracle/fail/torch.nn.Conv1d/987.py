import torch
arg_1 = 16
arg_2 = 960
arg_3_0 = 17
arg_3_1 = 63
arg_3_2 = -1
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = 2
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(0,16,[20, 0, 50], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
