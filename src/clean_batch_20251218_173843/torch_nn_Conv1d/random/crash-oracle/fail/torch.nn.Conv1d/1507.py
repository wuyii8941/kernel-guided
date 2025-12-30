import torch
arg_1 = 2
arg_2 = 16
arg_3 = False
arg_4 = "max"
arg_class = torch.nn.Conv1d(arg_1,arg_2,arg_3,stride=arg_4,)
arg_5_0_tensor = torch.randint(-256,32768,[64, 16, 50, 1], dtype=torch.int32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
