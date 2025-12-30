import torch
arg_1 = 1188
arg_2 = 10
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,2,[257, 1200], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
