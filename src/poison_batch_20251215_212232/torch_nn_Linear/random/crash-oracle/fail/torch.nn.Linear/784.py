import torch
arg_1 = 973
arg_2 = 42024
arg_3 = True
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.randint(-16,4,[0, 1, 1074], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
