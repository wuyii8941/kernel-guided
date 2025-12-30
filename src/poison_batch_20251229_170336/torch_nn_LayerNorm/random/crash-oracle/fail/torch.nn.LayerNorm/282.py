import torch
arg_1 = 1032
arg_2 = "max"
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.randint(0,2,[1, 0, 1024], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
