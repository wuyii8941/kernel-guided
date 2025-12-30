import torch
arg_1 = 20
arg_2 = 45
arg_3 = 12
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-1,64,[128], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([128, 30], dtype=torch.float16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
