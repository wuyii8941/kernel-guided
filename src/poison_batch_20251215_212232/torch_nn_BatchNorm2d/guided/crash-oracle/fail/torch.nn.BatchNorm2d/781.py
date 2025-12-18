import torch
arg_1 = 16
arg_2 = 1e-06
arg_class = torch.nn.BatchNorm2d(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.randint(0,4,[8, np.int64(16), 128, 263], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
