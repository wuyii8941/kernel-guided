import torch
arg_1 = -1
arg_2 = 1e+20
arg_3 = False
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.randint(-8,8,[11, 1, 1024], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
