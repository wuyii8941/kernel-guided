import torch
arg_1 = "max"
arg_2 = -4
arg_3 = 0.1
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([-1, 32, -1], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-128,2,[20, 32, 512], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.randint(0,32,[20, 32, 512, 8], dtype=torch.uint8)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
