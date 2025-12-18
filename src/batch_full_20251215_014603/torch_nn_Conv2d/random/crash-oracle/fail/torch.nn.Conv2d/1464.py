import torch
arg_1 = 1060
arg_2 = 2047
arg_3 = 8
arg_4 = False
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.randint(-128,128,[128, 1024, 0, 4, 0], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
