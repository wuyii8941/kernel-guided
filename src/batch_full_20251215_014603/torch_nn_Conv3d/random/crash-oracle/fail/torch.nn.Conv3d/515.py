import torch
arg_1 = 63
arg_2 = 54
arg_3_0 = 1.0
arg_3_1 = -1024.0
arg_3_2 = True
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4_0 = 2
arg_4_1 = 1
arg_4_2 = 1
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = False
arg_5_1 = False
arg_5_2 = 71.0
arg_5_3 = "reflect"
arg_5_4 = "max"
arg_5_5 = False
arg_5 = [arg_5_0,arg_5_1,arg_5_2,arg_5_3,arg_5_4,arg_5_5,]
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([20, 16, 10, 50, 100], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
