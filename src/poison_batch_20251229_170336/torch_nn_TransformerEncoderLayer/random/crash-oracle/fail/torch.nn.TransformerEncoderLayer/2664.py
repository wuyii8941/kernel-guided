import torch
arg_1 = -6.715747472149686
arg_2 = 13
arg_class = torch.nn.TransformerEncoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-32,256,[10, -1, 512], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
