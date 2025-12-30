import torch
arg_1 = 3
arg_2 = 0
arg_3 = 1
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-4,32,[128, 85, 32, 32], dtype=torch.int16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
