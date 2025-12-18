import torch
arg_1 = False
arg_2 = 32
arg_3_0 = 43
arg_3_1 = -53
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 39
arg_5 = False
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.randint(-128,16,[80, 128, 0, 32, 1], dtype=torch.int8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
