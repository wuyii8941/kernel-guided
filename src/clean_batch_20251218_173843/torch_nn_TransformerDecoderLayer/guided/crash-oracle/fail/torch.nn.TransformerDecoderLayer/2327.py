import torch
arg_1 = "max"
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-4,32,[73, 37, 512], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([26, 0, 568], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
