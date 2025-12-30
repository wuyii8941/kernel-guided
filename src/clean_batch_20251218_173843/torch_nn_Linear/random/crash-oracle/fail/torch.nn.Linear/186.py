import torch
arg_1 = 1200
arg_2 = 100.0
arg_3 = False
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.randint(-64,4,[1, 6, 1024], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
