import torch
arg_1 = 57
arg_2 = 63
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,2,[3, 0], dtype=torch.bool)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.rand([38, 82], dtype=torch.bfloat16)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
