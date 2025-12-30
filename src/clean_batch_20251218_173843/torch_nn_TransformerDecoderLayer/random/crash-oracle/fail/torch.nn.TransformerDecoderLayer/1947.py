import torch
arg_1 = 492
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-16,16,[20, 0, 462], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-64,2,[10, 32], dtype=torch.int16)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
