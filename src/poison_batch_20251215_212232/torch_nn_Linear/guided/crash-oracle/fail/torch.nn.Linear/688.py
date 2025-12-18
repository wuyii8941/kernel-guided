import torch
arg_1 = 1024
arg_2 = 31232
arg_3 = True
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.randint(0,32,[11, 5, 1018], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
