import torch
arg_1 = 1903
arg_2 = 66
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-1,8,[16, 1920], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
