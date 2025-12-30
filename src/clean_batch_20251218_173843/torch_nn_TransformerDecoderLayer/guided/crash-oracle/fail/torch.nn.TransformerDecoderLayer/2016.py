import torch
arg_1 = 1.0
arg_2 = 16
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-64,16384,[3, 1, 512], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(0,8,[0, 32], dtype=torch.uint8)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
