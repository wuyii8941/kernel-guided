import torch
arg_1 = 512
arg_2 = 1e+20
arg_class = torch.nn.TransformerEncoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-512,2048,[10, 35, 512], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
