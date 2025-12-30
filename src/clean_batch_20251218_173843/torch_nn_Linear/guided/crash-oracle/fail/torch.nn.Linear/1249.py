import torch
arg_1 = 1023
arg_2 = 31232
arg_3 = False
arg_class = torch.nn.Linear(arg_1,arg_2,bias=arg_3,)
arg_4_0_tensor = torch.rand([0, 1, 1057, 0], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
res = arg_class(*arg_4)
