import torch
arg_1 = 76
arg_2 = False
arg_3 = 3
arg_4 = -19
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-4096,2,[20, 0, 76], dtype=torch.int32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
