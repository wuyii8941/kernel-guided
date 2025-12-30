import torch
arg_1 = -29
arg_2 = 35.0
arg_3 = 60
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([141, 20], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-32,32768,[101], dtype=torch.int32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
