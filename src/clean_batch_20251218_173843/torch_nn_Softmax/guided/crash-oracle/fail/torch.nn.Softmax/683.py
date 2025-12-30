import torch
arg_1 = 2
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-512,8192,[37, 12], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
