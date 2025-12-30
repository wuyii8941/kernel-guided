import torch
arg_1 = -16
arg_2 = 1
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,).cuda()
arg_3_0_tensor = torch.rand([1024, 32, 512], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_tensor = torch.rand([0, 999, 512], dtype=torch.complex64)
arg_3_1 = arg_3_1_tensor.clone().cuda()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
