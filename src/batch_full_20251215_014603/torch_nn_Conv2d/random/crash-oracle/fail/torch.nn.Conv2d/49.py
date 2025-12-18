import torch
arg_1 = 2048
arg_2 = "replicate"
arg_3_tensor = torch.rand([40], dtype=torch.float32)
arg_3 = arg_3_tensor.clone()
arg_4 = 12
arg_class = torch.nn.Conv2d(arg_1,arg_2,bias=arg_3,kernel_size=arg_4,)
arg_5_0_tensor = torch.rand([69, 2048, 0, np.int64(16)], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
