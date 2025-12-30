import torch
arg_1 = 16
arg_2 = 47
arg_3_0 = 3
arg_3_1 = 5
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = -47
arg_4_1 = -31
arg_4 = [arg_4_0,arg_4_1,]
arg_5_0 = -41
arg_5_1 = 47
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.randint(-2048,8192,[20, 16, 112, 100], dtype=torch.int64)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
