import torch
arg_1 = 256
arg_2 = 256
arg_3 = 4
arg_4 = 2
arg_5 = -93.0
arg_6 = 0
arg_7 = False
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.randint(-2048,128,[1, 256, 28, 28], dtype=torch.int64)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
