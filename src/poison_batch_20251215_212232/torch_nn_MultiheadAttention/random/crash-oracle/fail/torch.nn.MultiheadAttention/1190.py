import torch
arg_1 = 512
arg_2 = 8
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(-32768,8,[20, 0, 512], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([12, 32], dtype=torch.bfloat16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(0,4,[20, 32, 491], dtype=torch.uint8)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
