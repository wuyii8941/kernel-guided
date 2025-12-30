import torch
arg_1 = 23
arg_2 = -22
arg_3 = 2
arg_4 = -44
arg_5 = 0
arg_6 = -70.0
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.randint(0,32,[8, 0, 128, 256], dtype=torch.uint8)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
