import torch
arg_1 = 3
arg_2_0 = 13.0
arg_2 = [arg_2_0,]
arg_3 = 1
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(-32768,1,[128, 384, 4], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
