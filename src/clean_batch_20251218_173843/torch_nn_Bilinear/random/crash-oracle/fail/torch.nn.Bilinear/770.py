import torch
arg_1 = 20
arg_2 = 30
arg_3 = 29
arg_class = torch.nn.Bilinear(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-16,4096,[148, 0], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([128, 30], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
