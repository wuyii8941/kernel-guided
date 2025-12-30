import torch
arg_1 = -2147483648
arg_2 = 8
arg_class = torch.nn.TransformerEncoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-32,16384,[10, 32, 516], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
