import torch
arg_1 = 16
arg_2 = 33
arg_3_0 = -45
arg_3_1 = -54
arg_3_2 = 1024
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4_0 = 26
arg_4_1 = -15
arg_4_2 = -16
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = 60
arg_5_1 = 0
arg_5_2 = 56
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.randint(-4,64,[20, 46, 10, 50, 0], dtype=torch.int8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
