import torch
arg_1 = 487
arg_2 = 39
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-256,512,[20, 0, 0], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-128,32,[12, 32, 479], dtype=torch.int8)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
