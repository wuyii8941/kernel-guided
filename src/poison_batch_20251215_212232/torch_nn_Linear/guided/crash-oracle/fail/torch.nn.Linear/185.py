import torch
arg_1 = -16
arg_2 = 1
arg_class = torch.nn.Linear(in_features=arg_1,out_features=arg_2,)
arg_3_0_tensor = torch.rand([75, 128], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
