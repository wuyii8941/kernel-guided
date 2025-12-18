import torch
arg_1 = -0.9252938720292461
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([2, 12, 8, 8, 1], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
