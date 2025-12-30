import torch
arg_1 = 512
arg_2 = True
arg_class = torch.nn.BatchNorm2d(arg_1,momentum=arg_2,)
arg_3_0_tensor = torch.randint(0,32,[0, 508, 7], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
