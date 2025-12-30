import torch
arg_1 = 512
arg_2 = 1
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,).cuda()
arg_3_0_tensor = torch.randint(0,32,[0, 32, 512], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_tensor = torch.randint(0,1,[10, -1, 512, 1], dtype=torch.uint8)
arg_3_1 = arg_3_1_tensor.clone().cuda()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
