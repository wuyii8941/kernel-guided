import torch
arg_1 = -31.0
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-2,128,[23, 12, 55, 0], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
