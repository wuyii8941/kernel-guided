import torch
arg_1 = 987
arg_2 = 3
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-32,8192,[64, 1], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
