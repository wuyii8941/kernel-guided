import torch
arg_1 = 502
arg_2 = "max"
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(0,2,[20, 16], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-2,32,[20, 1024, 512], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(0,256,[20, 0, 574], dtype=torch.uint8)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
