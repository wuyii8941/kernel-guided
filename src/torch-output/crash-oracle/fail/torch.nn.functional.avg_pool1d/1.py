import torch
arg_1_tensor = torch.rand([0, 16], dtype=torch.float16)
arg_1 = arg_1_tensor.clone()
arg_2 = 3
arg_3 = 2
arg_4 = 0
arg_5 = False
res = torch.nn.functional.avg_pool1d(arg_1,arg_2,arg_3,arg_4,arg_5,)
