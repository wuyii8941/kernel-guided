import torch
arg_1 = -1
arg_class = torch.nn.Softmax(dim=arg_1,)
arg_2_0_tensor = torch.randint(0,256,[27, 12, 0, 1024], dtype=torch.uint8)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
