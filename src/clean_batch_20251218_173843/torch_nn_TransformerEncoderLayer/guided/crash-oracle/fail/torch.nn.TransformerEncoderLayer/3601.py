import torch
arg_1 = 541
arg_2 = 1024
arg_class = torch.nn.TransformerEncoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-512,256,[10, 32, 512, 0], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
