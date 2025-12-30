import torch
arg_1 = -29
arg_2 = -16
arg_3 = 40
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(0,64,[128, 20], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([111, 30], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
