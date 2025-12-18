import torch
arg_1 = 16
arg_2 = 74
arg_3_0 = 3
arg_3_1 = 5
arg_3_2 = 2
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4_0 = 16
arg_4_1 = -28
arg_4_2 = -21
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = 4
arg_5_1 = 2
arg_5_2 = 0
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.randint(-1,4,[20, 16, 10, 50, 98, 1], dtype=torch.int8)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
