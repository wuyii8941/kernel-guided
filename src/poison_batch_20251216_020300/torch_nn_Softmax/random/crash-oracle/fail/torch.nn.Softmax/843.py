import torch
arg_1 = -1020.0533147804234
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([4, 12, 141], dtype=torch.complex64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
