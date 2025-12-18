import torch
arg_1_0 = "max"
arg_1_1 = "max"
arg_1_2 = 0.8234203954271724
arg_1_3 = "reflect"
arg_1 = [arg_1_0,arg_1_1,arg_1_2,arg_1_3,]
arg_class = torch.nn.LocalResponseNorm(arg_1,)
arg_2_0_tensor = torch.rand([32, 5, 24, 24], dtype=torch.float32)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
