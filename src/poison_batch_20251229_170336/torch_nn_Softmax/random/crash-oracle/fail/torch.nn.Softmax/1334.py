import torch
arg_1 = True
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([6, 12, 8, 0], dtype=torch.complex128)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
