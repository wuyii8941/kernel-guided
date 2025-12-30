import torch
arg_1_tensor = torch.rand([2], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = 1.0
arg_3 = False
res = torch.nn.functional.celu(arg_1,arg_2,arg_3,)
