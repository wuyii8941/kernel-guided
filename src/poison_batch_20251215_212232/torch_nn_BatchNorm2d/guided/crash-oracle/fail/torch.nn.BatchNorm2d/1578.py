import torch
arg_1 = 16
arg_2 = -35.15483986068185
arg_class = torch.nn.BatchNorm2d(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.rand([np.int64(16), 16, 69, 263], dtype=torch.bfloat16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
