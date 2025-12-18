import torch
arg_1 = 226
arg_2 = 940
arg_3 = True
arg_4 = 3
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,groups=arg_4,)
arg_5_0_tensor = torch.rand([80, np.int64(16), 0, 0, 1], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
