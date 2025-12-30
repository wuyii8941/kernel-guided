import torch
arg_1 = 3
arg_2 = 44
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,)
arg_3_0_tensor = torch.randint(0,64,[128, 351, 0, 30, 0, 1], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
