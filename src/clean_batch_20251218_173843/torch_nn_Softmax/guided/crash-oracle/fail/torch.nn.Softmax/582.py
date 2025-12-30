import torch
arg_1 = 91.0
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([3, 1, 25, 102], dtype=torch.bfloat16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
