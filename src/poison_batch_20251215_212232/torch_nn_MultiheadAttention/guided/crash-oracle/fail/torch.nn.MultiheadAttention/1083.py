import torch
arg_1 = 512
arg_2 = -16
arg_3 = 56.60207924300195
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-1,128,[0, 0], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,2,[20, 32, 512], dtype=torch.bool)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(-32768,32,[62, 32, 512], dtype=torch.int16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
