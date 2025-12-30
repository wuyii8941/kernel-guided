import torch
arg_1 = 960
arg_2 = -13.9
arg_class = torch.nn.BatchNorm2d(arg_1,momentum=arg_2,)
arg_3_0_tensor = torch.randint(0,256,[0, 244, 14, 14, 1], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
