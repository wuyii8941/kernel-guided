import torch
arg_1 = 534
arg_2 = 37.0
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-8,128,[10, 32, 512, 25], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([10, 32, 512], dtype=torch.float16)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
