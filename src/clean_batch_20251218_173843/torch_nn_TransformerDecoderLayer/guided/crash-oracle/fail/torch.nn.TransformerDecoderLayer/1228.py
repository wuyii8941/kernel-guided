import torch
arg_1 = -1
arg_2 = 1
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-16384,128,[0, 32, 512], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-256,64,[10, 32, 509], dtype=torch.int64)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
