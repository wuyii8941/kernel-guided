import torch
arg_1 = 512
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-8,128,[20, 32, 480, 1], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([44, 0, 480, 1], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
