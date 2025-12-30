import torch
arg_1_tensor = torch.rand([1, 64, 10, 9], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = 7
arg_3 = True
res = torch.nn.functional.adaptive_max_pool2d(arg_1,arg_2,arg_3,)
