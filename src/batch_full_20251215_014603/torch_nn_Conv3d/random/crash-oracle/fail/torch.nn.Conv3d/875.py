import torch
arg_1 = 16
arg_2 = -16
arg_3_0 = False
arg_3_1 = "sum"
arg_3_2 = -109.0
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = 1
arg_5_0 = "max"
arg_5_1 = -52.0
arg_5_2 = -4.0
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([77, 50, 0, 65, 100], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
