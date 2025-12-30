import torch
arg_class = torch.nn.Softmax2d()
arg_1_0_tensor = torch.rand([2, 3, 12, 13], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
