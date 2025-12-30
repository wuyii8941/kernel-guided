import torch
arg_1 = 57
arg_2 = 32
arg_3_0 = "max"
arg_3_1 = 67.0
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 25
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([1, 16, 6, 6], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
