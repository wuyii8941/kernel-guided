import torch
arg_1 = 16
arg_2 = 13
arg_3 = -50
arg_4 = 1
arg_5 = 0
arg_6 = 0
arg_7 = False
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([0, 16, 128, 316], dtype=torch.bfloat16)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
