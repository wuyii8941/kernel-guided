import torch
arg_1 = 14
arg_2 = 2
arg_3 = True
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,return_indices=arg_3,)
arg_4_0_tensor = torch.rand([1, 1, 4, 4], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
