import torch
arg_1 = 294
arg_2 = "max"
arg_3 = 1024
arg_4 = -45
arg_5 = 1
arg_6_0 = 0
arg_6_1 = 0
arg_6_2 = 0
arg_6 = [arg_6_0,arg_6_1,arg_6_2,]
arg_7 = False
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([1, 256, 14, 14], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
