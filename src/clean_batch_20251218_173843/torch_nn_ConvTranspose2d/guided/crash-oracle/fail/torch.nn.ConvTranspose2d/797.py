import torch
arg_1 = -19
arg_2 = -46
arg_3 = -27
arg_4 = "max"
arg_5 = 0
arg_6 = True
arg_7_tensor = torch.randint(0,4,[141], dtype=torch.uint8)
arg_7 = arg_7_tensor.clone()
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([8, 16, 128, 256], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
res = arg_class(*arg_8)
