import torch
arg_1 = 512
arg_2 = 17
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,).cuda()
arg_3_0_tensor = torch.rand([20, 1, 512], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_tensor = torch.randint(0,128,[0, 29, 512], dtype=torch.uint8)
arg_3_1 = arg_3_1_tensor.clone().cuda()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
