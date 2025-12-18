import torch
arg_1 = 1
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([1, 16, 6], dtype=torch.complex64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
