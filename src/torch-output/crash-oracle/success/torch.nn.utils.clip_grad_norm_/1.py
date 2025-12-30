import torch
arg_1_tensor = torch.rand([2, 2], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = 1e+20
arg_3 = 2.0
res = torch.nn.utils.clip_grad_norm_(parameters=arg_1,max_norm=arg_2,norm_type=arg_3,)
