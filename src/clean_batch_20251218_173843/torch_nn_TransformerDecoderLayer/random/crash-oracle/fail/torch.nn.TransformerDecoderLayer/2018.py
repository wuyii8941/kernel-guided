import torch
arg_1 = -7.0
arg_2 = 0
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.rand([69, 32, 454], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([10, 0, 519], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
