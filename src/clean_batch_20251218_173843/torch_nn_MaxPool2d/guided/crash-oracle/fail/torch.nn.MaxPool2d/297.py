import torch
arg_1 = 2
arg_2 = 2
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,)
arg_3_0_tensor = torch.randint(-2048,2048,[0, 256, 0, 8], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
