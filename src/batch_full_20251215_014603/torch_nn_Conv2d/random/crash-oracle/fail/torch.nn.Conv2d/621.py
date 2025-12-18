import torch
arg_1 = -1
arg_2 = 192
arg_3 = False
arg_4 = 0
arg_class = torch.nn.Conv2d(arg_1,arg_2,bias=arg_3,kernel_size=arg_4,)
arg_5_0_tensor = torch.randint(-16,8192,[0, 2048, 6, 0], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
