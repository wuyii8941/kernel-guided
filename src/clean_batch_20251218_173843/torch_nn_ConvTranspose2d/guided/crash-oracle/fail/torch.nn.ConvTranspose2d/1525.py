import torch
arg_1 = 42
arg_2 = True
arg_3 = 55
arg_4 = 2
arg_5 = -45
arg_6 = 0
arg_7 = False
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.randint(0,8,[8, 16, 128, 207], dtype=torch.uint8)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
