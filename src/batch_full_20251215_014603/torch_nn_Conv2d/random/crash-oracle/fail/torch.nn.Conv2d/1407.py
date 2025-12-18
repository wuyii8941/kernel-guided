import torch
arg_1 = 1024
arg_2 = 2048
arg_3 = 1
arg_4 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.randint(0,8,[111, 1024, 0, 0], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
