import torch
arg_1 = 512
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.rand([6, 32, 537, 1], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-1024,32,[32, 32, 500, 34], dtype=torch.int32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
