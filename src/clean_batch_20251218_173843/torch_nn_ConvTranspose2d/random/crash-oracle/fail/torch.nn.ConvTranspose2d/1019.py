import torch
arg_1 = 256
arg_2 = 256
arg_3_0 = -51
arg_3_1 = -13
arg_3_2 = -116
arg_3 = [arg_3_0,arg_3_1,arg_3_2,]
arg_4 = 2
arg_5 = 40
arg_6 = 0
arg_7 = False
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([1, 256, 14, 14], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
