import torch
arg_1 = 256
arg_2 = -1.5523679426246368
arg_class = torch.nn.BatchNorm2d(arg_1,momentum=arg_2,)
arg_3_0_tensor = torch.randint(-16,8,[0, 253, 56, 56], dtype=torch.int8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
