import torch
arg_1 = 504
arg_2 = 16
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,).cuda()
arg_3_0_tensor = torch.randint(0,2,[20, 32, 65536], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_tensor = torch.rand([10, 31, 0], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone().cuda()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
