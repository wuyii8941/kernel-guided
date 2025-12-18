import torch
arg_1 = 516
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(0,256,[20, 32, 506], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-32768,32,[12, np.int64(1024), 512], dtype=torch.int32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
