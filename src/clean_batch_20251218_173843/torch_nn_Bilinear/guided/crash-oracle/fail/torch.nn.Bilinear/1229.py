import torch
arg_1 = 20
arg_2 = 30
arg_3 = -19
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(0,2,[128, 20], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(0,1,[128, 30], dtype=torch.uint8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
