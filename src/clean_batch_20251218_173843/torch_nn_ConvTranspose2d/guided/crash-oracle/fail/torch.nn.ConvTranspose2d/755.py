import torch
arg_1 = 231
arg_2 = 246
arg_3 = -1
arg_4_0 = 43
arg_4_1 = -63
arg_4_2 = 43
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5 = 1
arg_6 = 0
arg_7 = False
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([0, 256, 14, 14, 1], dtype=torch.float16)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
