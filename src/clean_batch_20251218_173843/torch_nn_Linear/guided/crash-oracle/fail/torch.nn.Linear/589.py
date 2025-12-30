import torch
arg_1 = 210
arg_2 = 6830
arg_class = torch.nn.Linear(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([1, 31, 251], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
