import torch
arg_1 = 512
arg_2 = False
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.rand([20, 32], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(0,16,[0, 0, 512], dtype=torch.uint8)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
