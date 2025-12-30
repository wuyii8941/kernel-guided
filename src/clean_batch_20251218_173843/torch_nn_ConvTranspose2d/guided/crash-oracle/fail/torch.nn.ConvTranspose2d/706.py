import torch
arg_1 = 204
arg_2 = 275
arg_3 = 4
arg_4 = 2
arg_5_0 = 3
arg_5_1 = 1
arg_5 = [arg_5_0,arg_5_1,]
arg_6 = 18
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([1024, 0, 28, 28, 1], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
