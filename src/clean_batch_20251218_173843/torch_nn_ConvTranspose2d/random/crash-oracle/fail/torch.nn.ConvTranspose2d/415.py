import torch
arg_1 = 64
arg_2 = "reflect"
arg_3_0 = 2
arg_3_1 = 2
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 2
arg_5 = -40
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([65, 64, 14, 14], dtype=torch.bfloat16)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
res = arg_class(*arg_6)
