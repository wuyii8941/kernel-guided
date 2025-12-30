import torch
arg_1 = 16
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([3, 2, 6, 6, 1024], dtype=torch.float64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
