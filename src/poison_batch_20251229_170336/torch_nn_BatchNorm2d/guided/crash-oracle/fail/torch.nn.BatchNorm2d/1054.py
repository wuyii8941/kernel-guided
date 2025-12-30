import torch
arg_1 = 0.5543556080238083
arg_class = torch.nn.BatchNorm2d(arg_1,)
arg_2_0_tensor = torch.rand([1, 256, 88], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
