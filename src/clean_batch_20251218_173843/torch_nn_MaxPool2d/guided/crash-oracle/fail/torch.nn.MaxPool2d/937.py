import torch
arg_1_0 = 61
arg_1_1 = 55
arg_1 = [arg_1_0,arg_1_1,]
arg_2_0 = "max"
arg_2_1 = True
arg_2 = [arg_2_0,arg_2_1,]
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-128,32,[1, 256, 8, 30], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
