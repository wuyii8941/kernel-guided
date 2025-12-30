import torch
arg_1_tensor = torch.randint(-512,64,[5], dtype=torch.int64)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([10], dtype=torch.complex128)
arg_2 = arg_2_tensor.clone()
res = torch.ger(arg_1,arg_2,)
