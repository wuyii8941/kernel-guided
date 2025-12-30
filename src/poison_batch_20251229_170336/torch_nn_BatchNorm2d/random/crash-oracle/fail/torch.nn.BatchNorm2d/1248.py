import torch
arg_1 = -0.3845306061416549
arg_2 = -0.9935530714263224
arg_class = torch.nn.BatchNorm2d(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.rand([8, 16, 128, 256], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
