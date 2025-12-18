import torch
arg_1 = 100
arg_2 = True
arg_class = torch.nn.BatchNorm3d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-16384,4,[20, 100, 35, np.int64(16), 10], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
