import torch
arg_1 = 3
arg_2 = 1
arg_3 = 41
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.randint(0,4,[1, 64, 112, 112], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
