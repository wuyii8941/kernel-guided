import torch
arg_1 = -21
arg_2 = 33
arg_3 = -36
arg_4 = -4
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(0,4,[20, 72, 50, 1], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
