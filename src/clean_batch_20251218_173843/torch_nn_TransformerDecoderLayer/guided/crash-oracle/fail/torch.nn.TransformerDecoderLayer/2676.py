import torch
arg_1 = 512
arg_2 = 65
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-4,8,[20, 63, 478], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([0, 32, 512, 1], dtype=torch.complex64)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
