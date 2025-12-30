import torch
arg_1 = 37.0
arg_2 = 60
arg_3 = 84
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-1,512,[128, 20], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,128,[188], dtype=torch.uint8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
