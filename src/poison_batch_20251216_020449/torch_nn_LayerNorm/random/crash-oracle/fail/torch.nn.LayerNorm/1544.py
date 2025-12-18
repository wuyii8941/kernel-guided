import torch
arg_1_0 = 384
arg_1 = [arg_1_0,]
arg_2 = -3.0730231808070716
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.randint(0,32,[16, 6, 128], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
