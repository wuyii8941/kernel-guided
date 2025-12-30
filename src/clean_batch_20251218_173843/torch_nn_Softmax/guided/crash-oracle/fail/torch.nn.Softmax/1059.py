import torch
arg_1 = -63
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([16, 16, 6, 17, 1], dtype=torch.float16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
