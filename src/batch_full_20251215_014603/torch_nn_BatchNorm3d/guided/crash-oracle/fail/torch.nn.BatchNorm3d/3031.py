import torch
arg_1 = 100
arg_2 = 56.0
arg_class = torch.nn.BatchNorm3d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.rand([np.int64(16), 100, 74, 79, 10], dtype=torch.complex128)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
