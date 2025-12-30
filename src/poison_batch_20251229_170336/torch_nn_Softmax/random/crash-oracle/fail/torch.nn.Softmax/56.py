import torch
arg_1 = 3
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-2,8,[4, 10, 1024, 141], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
