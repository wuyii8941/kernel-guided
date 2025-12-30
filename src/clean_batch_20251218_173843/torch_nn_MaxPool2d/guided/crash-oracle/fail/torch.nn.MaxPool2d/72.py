import torch
arg_1_0 = 3
arg_1_1 = 5
arg_1_2 = 2
arg_1 = [arg_1_0,arg_1_1,arg_1_2,]
arg_2 = 16
arg_3 = 1
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(-16,1,[149, 1069, 0, 0, 56], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
