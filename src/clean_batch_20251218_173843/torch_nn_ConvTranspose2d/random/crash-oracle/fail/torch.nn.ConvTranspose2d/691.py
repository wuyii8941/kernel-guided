import torch
arg_1 = 256
arg_2 = 260
arg_3 = 4
arg_4 = 2
arg_5 = -17
arg_6 = 0
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.randint(-256,8192,[1, 205, 28, 79], dtype=torch.int32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
