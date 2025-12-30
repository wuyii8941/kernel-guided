import torch
arg_1 = 128
arg_2 = 1.9048276299501987
arg_class = torch.nn.LayerNorm(arg_1,eps=arg_2,)
arg_3_0_tensor = torch.randint(0,2,[-1, 6, 131], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
