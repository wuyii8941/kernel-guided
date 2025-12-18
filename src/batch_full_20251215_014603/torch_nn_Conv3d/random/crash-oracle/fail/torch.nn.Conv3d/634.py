import torch
arg_1 = -3
arg_2 = 33
arg_3_0 = 44.0
arg_3_1 = False
arg_3_2 = 0.0
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4_0 = 2
arg_4_1 = 1
arg_4_2 = 1
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = 1
arg_5_1 = -95
arg_5_2 = 44
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_class = torch.nn.Conv3d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([np.int64(16), 16, 10, 50], dtype=torch.bfloat16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
