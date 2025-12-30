import torch
arg_1 = 20
arg_2 = 30
arg_3 = 77
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-8,16384,[128, 0, 1], dtype=torch.int32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-4,256,[128], dtype=torch.int16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
