import torch
arg_1 = 818
arg_2 = 100
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-256,1,[16], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
