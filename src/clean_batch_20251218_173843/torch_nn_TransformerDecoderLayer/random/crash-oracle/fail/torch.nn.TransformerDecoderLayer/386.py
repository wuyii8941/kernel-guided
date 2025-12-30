import torch
arg_1 = 515
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(0,2,[0, 32, 0, 1], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-2,8,[1, 47, 1, 55], dtype=torch.int8)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
