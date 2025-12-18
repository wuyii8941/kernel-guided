import torch
arg_1 = -1.870914142061821
arg_2 = 63
arg_3_tensor = torch.rand([40], dtype=torch.float32)
arg_3 = arg_3_tensor.clone()
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.rand([11, 5, 1024], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
