import torch
arg_1 = 520
arg_2 = -1024
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,).cuda()
arg_3_0_tensor = torch.randint(-32768,4096,[512, 35, 517], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_tensor = torch.rand([2, 8, 512], dtype=torch.float32)
arg_3_1 = arg_3_1_tensor.clone().cuda()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
