import torch
arg_1 = 3
arg_2 = 57
arg_3 = 1
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(-1,8,[128, 0, 8], dtype=torch.int8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
