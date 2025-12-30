import torch
arg_1 = -60.083502096417945
arg_class = torch.nn.BatchNorm1d(arg_1,)
arg_2_0_tensor = torch.rand([64, 12544], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
