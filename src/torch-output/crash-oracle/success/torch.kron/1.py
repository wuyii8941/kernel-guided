import torch
arg_1_tensor = torch.rand([3, 6, 3072], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([10, 20], dtype=torch.float64)
arg_2 = arg_2_tensor.clone()
res = torch.kron(arg_1,arg_2,)
