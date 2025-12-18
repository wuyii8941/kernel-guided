import torch
arg_1 = True
arg_2 = 1.0
arg_3 = 1024
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,)
arg_4_0_tensor = torch.randint(-4,32,[80, 832, 41, 4], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
