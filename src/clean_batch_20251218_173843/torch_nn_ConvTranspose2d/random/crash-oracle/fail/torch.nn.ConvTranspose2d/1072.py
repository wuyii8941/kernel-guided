import torch
arg_1 = 308
arg_2 = 289
arg_3 = -20
arg_4 = 2
arg_5 = 1
arg_6 = -49
arg_7_tensor = torch.rand([33], dtype=torch.float32)
arg_7 = arg_7_tensor.clone()
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([1, 256, 14, 14], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
