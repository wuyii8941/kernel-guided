import torch
arg_1 = -27
arg_2 = 33
arg_3 = 3
arg_4_0 = "sum"
arg_4_1 = True
arg_4 = [arg_4_0,arg_4_1,]
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-128,2,[20, 16, 50], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
