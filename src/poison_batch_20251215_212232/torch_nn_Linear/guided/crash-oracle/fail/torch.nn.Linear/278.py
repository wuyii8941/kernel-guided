import torch
arg_1 = 1024
arg_2 = 31236
arg_3 = True
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.randint(0,2,[11, 7, 1024], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
