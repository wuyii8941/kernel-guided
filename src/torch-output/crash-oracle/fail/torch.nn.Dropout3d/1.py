import torch
arg_1 = -44.8
arg_class = torch.nn.Dropout3d(p=arg_1,)
arg_2_0_tensor = torch.rand([20, 16, 4, 32, 32], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
