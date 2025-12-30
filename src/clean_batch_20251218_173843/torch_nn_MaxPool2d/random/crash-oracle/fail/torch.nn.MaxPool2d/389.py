import torch
arg_1 = 3
arg_2 = 1
arg_3 = 1
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(0,2,[16, 0, 66, 16], dtype=torch.bool)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
