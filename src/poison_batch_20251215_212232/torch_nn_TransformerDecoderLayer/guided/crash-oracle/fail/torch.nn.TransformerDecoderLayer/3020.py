import torch
arg_1 = 512
arg_2 = 4
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.rand([6, 0, 512], dtype=torch.complex128)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-512,256,[61, 32, 471], dtype=torch.int32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
