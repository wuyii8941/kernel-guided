import torch
arg_1 = 62
arg_2 = 34
arg_3 = 2
arg_4 = 2
arg_5 = -2
arg_6_0 = 0
arg_6_1 = 0
arg_6 = [arg_6_0,arg_6_1,]
arg_7 = "replicate"
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([8, 16, 128, 256], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
