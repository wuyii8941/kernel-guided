import torch
arg_1 = -1024
arg_2 = 29
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-128,64,[20, 56, 540], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(0,2,[10, 0], dtype=torch.bool)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
