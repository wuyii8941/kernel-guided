import torch
arg_1 = 0
arg_2 = 0.001
arg_class = torch.nn.BatchNorm2d(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.randint(0,32,[8, 16, 128, 256], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
