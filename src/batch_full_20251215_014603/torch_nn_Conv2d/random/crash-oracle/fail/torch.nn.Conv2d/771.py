import torch
arg_1 = 548
arg_2 = 2075
arg_3 = 1
arg_4_tensor = torch.rand([33], dtype=torch.float32)
arg_4 = arg_4_tensor.clone()
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,bias=arg_4,)
arg_5_0_tensor = torch.rand([np.int64(16), 512, 16, 16], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
