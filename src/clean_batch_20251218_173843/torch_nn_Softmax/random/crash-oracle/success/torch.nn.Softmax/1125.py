import torch
arg_1 = -1
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(-64,1,[0, 16, 6], dtype=torch.int8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
