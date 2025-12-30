import torch
arg_1 = 512
arg_2 = -4.493249746740185
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,).cuda()
arg_3_0_tensor = torch.randint(-512,128,[24, 0, 507], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_tensor = torch.randint(-4096,64,[10, 0], dtype=torch.int64)
arg_3_1 = arg_3_1_tensor.clone().cuda()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
