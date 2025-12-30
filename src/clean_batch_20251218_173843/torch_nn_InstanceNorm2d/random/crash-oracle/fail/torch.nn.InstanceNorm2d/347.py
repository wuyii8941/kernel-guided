import torch
arg_1 = True
arg_2 = "max"
arg_class = torch.nn.InstanceNorm2d(arg_1,affine=arg_2,)
arg_3_0_tensor = torch.randint(-16,1024,[20, 60, 35, 37], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
