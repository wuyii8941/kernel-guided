import torch
arg_1 = 1024
arg_2 = 42024
arg_3 = False
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.randint(-4096,1024,[980, 0, 1029], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
