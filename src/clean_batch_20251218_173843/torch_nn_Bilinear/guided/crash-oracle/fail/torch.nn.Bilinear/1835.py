import torch
arg_1 = 20
arg_2 = 10.0
arg_3 = 40
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(0,2,[112, 20, 1], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([128, 30], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
