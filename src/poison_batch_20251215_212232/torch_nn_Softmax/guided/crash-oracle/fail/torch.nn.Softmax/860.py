import torch
arg_1 = -12.326673242771763
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.rand([2, 3], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
