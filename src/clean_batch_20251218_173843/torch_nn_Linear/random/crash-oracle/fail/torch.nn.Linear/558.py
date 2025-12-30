import torch
arg_1 = 1024
arg_2 = 100
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-32,8,[16, 1024, 1], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
