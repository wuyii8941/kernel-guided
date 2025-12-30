import torch
arg_1 = 16
arg_2 = -8
arg_3 = 2
arg_4 = 2
arg_5_0 = -61
arg_5_1 = 43
arg_5_2 = 46
arg_5_3 = 0
arg_5_4 = -1
arg_5_5 = -15
arg_5 = [arg_5_0,arg_5_1,arg_5_2,arg_5_3,arg_5_4,arg_5_5,]
arg_6 = 0
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([8, 16, 128, 256], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
