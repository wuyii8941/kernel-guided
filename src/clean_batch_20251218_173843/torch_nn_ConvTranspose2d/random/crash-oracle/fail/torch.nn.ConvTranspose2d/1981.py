import torch
arg_1 = 16
arg_2 = 73
arg_3 = 4
arg_4 = 1024
arg_5 = 1
arg_6 = -23
arg_7 = False
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.randint(-4,256,[9, 0, 28, 15], dtype=torch.int16)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
