import torch
arg_1_tensor = torch.rand([2], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = True
res = torch.nn.functional.hardsigmoid(arg_1,arg_2,)
