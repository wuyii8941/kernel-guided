import torch
arg_1 = 100
arg_2 = True
arg_class = torch.nn.InstanceNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-8,32,[15, 100, 35, 256], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
